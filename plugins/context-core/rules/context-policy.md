# Context capture policy

- 매 user turn의 새 의미를 한 번 내부 audit한다. 선택·전제·용어가 확정되는 순간, 이전 맥락이 판단을 바꿀 때만 metadata-first로 recall한다. durable signal이 없으면 audit 상태나 capture 질문을 표시하지 않는다.
- semantic owner는 관련 실제 본문·scope·rationale를 비교한다. conflict 또는 rationale change는 primary 결론 전에 관련 artifact와 차이를 알린다.
- 그 외에는 원 답변을 먼저 마치고 성숙한 durable 후보만 milestone당 한 번 제안한다. 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다.
- 사용자가 complete preview 본문의 capture 질문에 직접적·명시적·무조건적 긍정으로 답한 뒤에만 쓴다. `알겠어` 단독, 조건·수정 요청·화제 전환은 승인이 아니며 승인 뒤 재생성하지 않는다.

Agent는 preview stdout의 `approval_digest`를 변경 없이 apply에 전달하고, frozen receipt·repository identity·core SHA·CAS·lock·atomic-write 검증을 그대로 유지한다. 이 transport 정보는 사용자에게 보이거나 입력을 요구하지 않는다.
