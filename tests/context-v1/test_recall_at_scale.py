"""Frozen near-topic regressions; full record-based measurements live in v4."""
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[2]
CLI = ROOT / "plugins/context-decision/skills/decision/scripts/decision_cli.py"
SPEC = importlib.util.spec_from_file_location("context_scale_recall", CLI)
decision_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(decision_cli)
FIXTURE = json.loads((pathlib.Path(__file__).parent / "fixtures/recall-scale.json").read_text())


def distractors(count: int) -> list[dict]:
    rows = []
    for number in range(count):
        row = copy.deepcopy(FIXTURE["distractors"][number % len(FIXTURE["distractors"])])
        row["id"] = f"ctx_{number:032x}"
        row["path"] = f"context/decision/distractor-{number:04d}.md"
        row["decision_key"] += f"-{number}"
        rows.append(row)
    return rows


class RecallAtScaleTests(unittest.TestCase):
    def test_all_eight_unmodified_queries_survive_near_topic_crowding(self) -> None:
        for count in (200, 1000):
            first = 0
            for case in FIXTURE["cases"]:
                with self.subTest(count=count, scenario=case["scenario_id"]):
                    target = case["target"]
                    rows = [*distractors(count), target]
                    before = copy.deepcopy(rows)

                    def read(_repo, row):
                        return {"id": row["id"], "path": row["path"], "sha256": "sha256:" + "a" * 64,
                                "frontmatter": row,
                                "sections": case["sections"] if row["id"] == target["id"] else {
                                    "Decision": row["title"], "Rationale": row["summary"],
                                    "Rejected alternatives": "An alternative recorded in the synthetic corpus.",
                                }}

                    with (mock.patch.object(decision_cli, "_index", return_value=("fixture index", rows, [])),
                          mock.patch.object(decision_cli, "_record", side_effect=read) as opened):
                        result = decision_cli.prepare_decision_check(ROOT, statement=case["statement"])
                    current = result["comparison_input"]["current"]
                    ids = [item["id"] for item in current]
                    self.assertIn(target["id"], ids, [item["title"] for item in current])
                    first += ids[0] == target["id"]
                    self.assertLessEqual(opened.call_count, 8)
                    self.assertLessEqual(len(decision_cli.canonical_json(result).encode()), 32768)
                    self.assertEqual(rows, before)
                    self.assertEqual("discovery_only", result["coverage"])
                    self.assertFalse(result["physical_write"])
            self.assertGreaterEqual(first, 6, f"N={count} recall@1={first}/8")

    def test_high_frequency_words_and_unknown_query_open_no_bodies(self) -> None:
        rows = distractors(1000)
        for row in rows:
            row["title"] += " ubiquitous"
        for statement in ("ubiquitous", "quasar zeppelin"):
            with self.subTest(statement=statement):
                with (mock.patch.object(decision_cli, "_index", return_value=("fixture index", rows, [])),
                      mock.patch.object(decision_cli, "_record") as opened):
                    result = decision_cli.prepare_decision_check(ROOT, statement=statement)
                opened.assert_not_called()
                self.assertEqual(0, result["retrieval"]["returned"])

    def test_common_inflections_match_existing_persisted_stems(self) -> None:
        for left, right in (("preserve", "preserving"), ("replace", "replacing"),
                            ("boundary", "boundaries"), ("module", "modules")):
            with self.subTest(words=(left, right)):
                stem = decision_cli.stem_token(left)
                self.assertEqual(stem, decision_cli.stem_token(right))
                self.assertEqual(stem, decision_cli.stem_token(stem))


if __name__ == "__main__":
    unittest.main()
