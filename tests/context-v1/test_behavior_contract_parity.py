#!/usr/bin/env python3
"""Pin the behavior gate across shipped English, Korean, policy, protocol, and host surfaces."""
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def prompts(plugin: str) -> str:
    manifest = json.loads(read(f"plugins/{plugin}/.codex-plugin/plugin.json"))
    return " ".join(manifest["interface"]["defaultPrompt"])


CORE_EN = (
    "AGENTS.md",
    "plugins/context-core/rules/context-policy.md",
    "plugins/context-core/skills/context/scripts/context_cli.py",
    "plugins/context-core/skills/context/SKILL.md",
    "plugins/context-core/skills/context/references/context-protocol.md",
)
CORE_KO = (
    "plugins/context-core/skills/context/SKILL.ko.md",
    "plugins/context-core/skills/context/references/context-protocol.ko.md",
)
DECISION_EN = (
    "plugins/context-decision/skills/decision/SKILL.md",
    "plugins/context-decision/rules/decision-policy.md",
    "plugins/context-decision/README.md",
    "plugins/context-decision/skills/decision/references/decision-protocol.md",
)
DECISION_KO = (
    "plugins/context-decision/skills/decision/SKILL.ko.md",
    "plugins/context-decision/README.ko.md",
    "plugins/context-decision/skills/decision/references/decision-protocol.ko.md",
)


class BehaviorContractParityTests(unittest.TestCase):
    def assert_all(self, paths: tuple[str, ...], markers: tuple[str, ...]) -> None:
        for relative in paths:
            body = read(relative).casefold()
            for marker in markers:
                with self.subTest(surface=relative, marker=marker):
                    self.assertIn(marker.casefold(), body)

    def test_mechanical_edit_zero_path_is_explicit_and_target_scoped(self) -> None:
        self.assert_all(
            CORE_EN[:3],
            (
                "mechanical local edit", "skip AGENTS/guidance discovery", "exclude `context/`",
                "request names a path", "infer one conventional task subtree",
                "search it once", "exact file", "never use `.`", "`--hidden`",
                "repository-wide globs", "repository root", "ask for the path instead of widening",
                "zero context tool calls",
                "zero `context/` artifact", "zero context mentions",
            ),
        )
        self.assert_all(
            (CORE_EN[3],),
            (
                "mechanical local edit", "skips AGENTS/guidance discovery", "excludes `context/`",
                "named path", "infer one task subtree",
                "search once", "exact file", "never use `.`", "`--hidden`",
                "repo-wide globs", "root", "ask for the path instead of widening",
                "context tool calls",
                "`context/` reads", "context mentions at zero", "session-only ledger",
                "actual bodies remain in context",
            ),
        )
        self.assert_all(
            (CORE_EN[4],),
            (
                "mechanical edit", "skip AGENTS/guidance discovery", "exclude `context/`",
                "named path only", "infer one conventional task subtree",
                "search it once", "exact file", "never use `.`", "`--hidden`",
                "repository-wide globs", "repository root", "ask for the path instead of widening",
                "context tool calls", "`context/` artifact reads", "context mentions at zero",
            ),
        )
        self.assert_all(
            CORE_KO,
            (
                "기계적", "AGENTS/guidance 탐색을 생략", "`context/`를 제외",
                "요청에 path가", "task noun", "한 번만", "exact file",
                "`--hidden`", "repository root", "범위를 넓히지 말고 path", "context tool call",
                "`context/` artifact read", "context 언급",
            ),
        )
        core_prompt = prompts("context-core")
        for marker in (
            "Mechanical pathless: search one inferred subtree",
            "no root/hidden/AGENTS/`context/`",
            "unsafe→ask", "calls/reads/mentions=0",
            "Recall index→body→mention→question",
        ):
            self.assertIn(marker, core_prompt)

    def test_four_step_intervention_ladder_has_en_ko_protocol_parity(self) -> None:
        for relative in CORE_EN[:3]:
            ladder = next(line for line in read(relative).splitlines() if "silent index check" in line)
            positions = [ladder.index(marker) for marker in ("silent index check", "matched body read", "action-changing mention", "required question")]
            self.assertEqual(sorted(positions), positions, relative)
        for relative in (CORE_EN[3], CORE_EN[4]):
            ladder = next(line for line in read(relative).splitlines() if "silent index check" in line)
            positions = [ladder.index(marker) for marker in ("silent index check", "selected body read", "user mention", "question")]
            self.assertEqual(sorted(positions), positions, relative)
        for relative in CORE_KO:
            ladder = next(line for line in read(relative).splitlines() if "조용한 index 확인" in line)
            ladder = ladder[ladder.index("조용한 index 확인"):]
            positions = [ladder.index(marker) for marker in ("조용한 index 확인", "선택", "사용자 언급", "질문")]
            self.assertEqual(sorted(positions), positions, relative)

    def test_hold_keep_supersede_and_revisit_boundaries_reach_every_surface(self) -> None:
        self.assert_all(
            CORE_EN,
            ("hold the affected action", "keep means", "not performed", "supersede", "explicit choice", "reassessment, not implementation", "decision payload", "storage"),
        )
        self.assert_all(
            CORE_KO,
            ("행동을 보류", "keep이면 수행하지", "supersede", "명시적 선택 뒤에만", "재평가 권한", "구현 권한", "decision payload", "저장"),
        )
        self.assert_all(
            DECISION_EN,
            ("hold", "keep means", "not performed", "supersede", "explicit choice", "reassessment, not implementation", "decision payload", "second storage"),
        )
        self.assert_all(
            DECISION_KO,
            ("보류", "keep이면 수행하지", "supersede", "명시적 선택 뒤에만", "재평가 권한", "구현 권한", "decision payload", "별도 저장"),
        )
        decision_prompt = prompts("context-decision")
        for marker in (
            "keep=not done",
            "ask keep=not done/supersede",
            "Say satisfied|no evidence|ambiguous",
            "Action≠evidence",
            "unrelated→no evidence",
            "relevant partial→ambiguous",
            "Explicit choice authorizes capture",
            "no second storage question",
            "transport private",
        ):
            self.assertIn(marker, decision_prompt)

    def test_check_actual_sections_and_revisit_classification_have_surface_parity(self) -> None:
        for relative in DECISION_EN:
            body = read(relative)
            for marker in (
                "Decision", "Rationale", "Rejected alternatives", "Revisit conditions",
                "satisfied", "no evidence", "ambiguous", "requested conflicting action",
                "explicit binary question", "verbatim",
            ):
                with self.subTest(surface=relative, marker=marker):
                    self.assertIn(marker, body)
            for marker in ("condition", "no evidence", "incomplete", "conflicting"):
                with self.subTest(surface=relative, taxonomy=marker):
                    self.assertIn(marker, body)
        for relative in DECISION_KO:
            body = read(relative)
            for marker in (
                "Decision", "Rationale", "Rejected alternatives", "Revisit conditions",
                "satisfied", "no evidence", "ambiguous", "요청된 충돌 행동 자체는 근거",
                "명시적 양자 질문", "user response에 그대로",
            ):
                with self.subTest(surface=relative, marker=marker):
                    self.assertIn(marker, body)
            for marker in ("다른 쟁점", "저장 조건", "no evidence", "불완전", "충돌"):
                with self.subTest(surface=relative, taxonomy=marker):
                    self.assertIn(marker, body)
        shipped_revisit = "\n".join(read(relative) for relative in (*DECISION_EN, *DECISION_KO))
        shipped_revisit += "\n" + read("plugins/context-decision/skills/decision/scripts/decision_cli.py")
        for fixture_coaching in ("growth priority", "offline-status", "offline status", "growth≠"):
            self.assertNotIn(fixture_coaching, shipped_revisit.casefold())
        skill = read("plugins/context-decision/skills/decision/SKILL.md")
        self.assertIn("run one exact-slot `decision_cli.py check`", skill)
        self.assertIn("Reuse sections returned by `check` in the same turn", skill)
        self.assertIn("do not call `read`, `spec-view`, or another context read", skill)
        decision_prompt = prompts("context-decision")
        self.assertIn("One check", decision_prompt)
        self.assertIn("quote/reuse actual sections", decision_prompt)
        self.assertIn("no reread", decision_prompt)
        self.assertIn("Say satisfied|no evidence|ambiguous", decision_prompt)
        self.assertIn("Action≠evidence", decision_prompt)
        self.assertIn("unrelated→no evidence", decision_prompt)
        self.assertIn("relevant partial→ambiguous", decision_prompt)
        self.assertIn("ask keep=not done/supersede", decision_prompt)

    def test_one_check_and_no_reread_are_pinned_on_public_surfaces(self) -> None:
        expected = {
            "plugins/context-decision/skills/decision/SKILL.md": ("one exact-slot `decision_cli.py check`", "another context read"),
            "plugins/context-decision/rules/decision-policy.md": ("run one exact-slot `check`", "without another context read"),
            "plugins/context-decision/README.md": ("one exact `check`", "without another context read"),
            "plugins/context-decision/skills/decision/references/decision-protocol.md": ("make one exact check", "without another read"),
            "plugins/context-decision/skills/decision/SKILL.ko.md": ("exact-slot `decision_cli.py check`를 한 번만", "다른 context read를 다시 호출하지 않는다"),
            "plugins/context-decision/README.ko.md": ("exact `check`를 한 번", "다른 context read 없이"),
            "plugins/context-decision/skills/decision/references/decision-protocol.ko.md": ("exact check를 한 번만", "다시 읽지 않고 재사용"),
        }
        for relative, markers in expected.items():
            body = read(relative)
            for marker in markers:
                with self.subTest(surface=relative, marker=marker):
                    self.assertIn(marker, body)

    def test_semantic_approval_and_transport_integrity_remain_separate(self) -> None:
        for relative in (
            "plugins/context-core/skills/context/SKILL.md",
            "plugins/context-decision/skills/decision/SKILL.md",
            "plugins/context-decision/rules/decision-policy.md",
        ):
            body = read(relative)
            for marker in ("approval_digest", "unchanged", "semantic delta", "same response"):
                with self.subTest(surface=relative, marker=marker):
                    self.assertIn(marker, body)
            self.assertNotIn("complete rendered body", body)
            self.assertNotIn("specific capture question", body)
        self.assertIn("Core alone owns final validation and writes", read("plugins/context-decision/skills/decision/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
