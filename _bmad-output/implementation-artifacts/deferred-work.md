- source_spec: `_bmad-output/implementation-artifacts/spec-epic-7-remove-unreachable-no-legal-move-flow.md`
  summary: Harden both validators by recomputing the canonical legal-destination set for caller-fabricated resolved states.
  evidence: Review demonstrated that a non-empty, empty-square move list with the correct dice target can still substitute unrelated destinations because placement trusts stored legal moves; this broader state-authenticity issue predates removal of the empty-list pass flow.
- source_spec: `_bmad-output/implementation-artifacts/spec-epic-7-remove-unreachable-no-legal-move-flow.md`
  summary: Add a shared cross-edition fixture corpus that directly compares Python and browser post-roll results.
  evidence: Each engine independently covers the same rule categories and all 36 initial-board rolls, but no single test currently normalizes and compares both implementations' boards, reserves, targets, and legal sets.
- source_spec: `_bmad-output/implementation-artifacts/spec-epic-7-remove-unreachable-no-legal-move-flow.md`
  summary: Expand invariant testing to generated reachable full-game trajectories and additional dense representative positions.
  evidence: Current exhaustive roll coverage begins from the official initial state while curated dense/capture-heavy positions are exercised by scenario and AI tests rather than exhaustive trajectory generation.
