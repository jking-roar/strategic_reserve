---
title: 'Complete Browser Game'
type: 'feature'
created: '2026-07-25'
status: 'done'
review_loop_iteration: 0
baseline_commit: '0d0fd574b438f8e17c7e1421dcd657aec86cada9'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The GitHub Pages workflow publishes only a placeholder, so visitors cannot play Strategic Reserve in a browser despite the browser edition being the project's first delivery priority.

**Approach:** Replace the placeholder with a complete, responsive, accessible static game supporting local two-player and two browser-AI modes, while keeping rules state authoritative and independently testable.

## Boundaries & Constraints

**Always:** Use repository-hosted, project-subpath-safe static assets with no backend or build-time runtime requirement. Red starts from the near/bottom side and Blue from the far/top side; map dice from the active player's perspective. Require the active player to initiate every roll. If no legal placement exists, announce it and require an explicit Pass/acknowledgment action before advancing. Revalidate every human or AI move before mutation; announce meaningful state changes; provide pointer and keyboard parity, visible focus, semantic labels, and non-color-only board states. Keep README attribution and distinguish the HTML and planned Python/Tkinter editions.

**Ask First:** Any rule change, any network or third-party runtime dependency, changing the existing Pages publishing root/workflow, or omitting an AI difficulty or accessibility requirement.

**Never:** Assume domain-root hosting; mutate authoritative state from rendering or AI evaluation; auto-roll, auto-pass a no-move turn, rely on color alone, attempt to close the browser tab, or remove/replace the planned Python edition.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Normal turn | User rolls; target is empty, friendly, or enemy | Resolve captures, show target/legal squares, accept one legal placement, update reserves, then alternate | Ignore illegal/stale activation and announce concise feedback without partial mutation |
| No legal play | Resolved target yields no destination | Explain the no-play state and expose a focused Pass/acknowledgment control | Do not advance until acknowledged; do not decrement reserve |
| Victory | Active player places their last reserve checker | Announce winner immediately, disable board/roll input, expose New Game | Prevent further state mutation |
| AI turn | PvC with rudimentary or advanced difficulty | AI initiates its roll and submits a validated legal move or explicitly passes | Bound work, preserve input state, and recover to a safe announced state if no move exists |
| Quit active game | User chooses Quit Game | Confirm; Yes returns to setup and No/Escape resumes unchanged | Never claim to close the browser tab |

</frozen-after-approval>

## Code Map

- `site/index.html` -- resilient semantic shell, controls, board/status regions, attribution, and relative asset entry points.
- `site/styles.css` -- responsive flat board-game presentation and accessible interaction/state treatments.
- `site/js/game-engine.js` -- authoritative initialization, perspective mapping, groups, roll resolution, legal moves, captures, placement, pass, and victory rules.
- `site/js/ai.js` -- non-mutating random and bounded 36-outcome strategic move selection.
- `site/js/app.js` -- setup/game controller, rendering, keyboard behavior, dialogs, announcements, and AI scheduling.
- `site/tests/*.test.js` -- deterministic engine, AI, DOM/static-contract, and edge-case coverage.
- `README.md` -- prominent published-game link and HTML/Python edition explanation.
- `package.json` -- dependency-free reproducible test/check commands if needed.

## Tasks & Acceptance

**Execution:**
- [x] `site/index.html`, `site/styles.css` -- build the progressively understandable responsive game shell and all required visual/focus states.
- [x] `site/js/game-engine.js` -- implement official setup and complete turn rules as pure, testable state transitions, including explicit no-play acknowledgment.
- [x] `site/js/ai.js` -- implement safe random play and time-bounded strategic evaluation that considers all 36 next-roll outcomes.
- [x] `site/js/app.js` -- connect setup, user-initiated rolls, PvP/PvC turns, accessible board input, live status, victory, restart, and quit confirmation.
- [x] `site/tests/*.test.js`, `package.json` -- cover the matrix, invariants, perspective conversion, captures, AI legality/non-mutation, static subpath safety, and key accessibility contracts.
- [x] `README.md`, `site/README.md` -- document the playable site, editions, controls, static layout, and verification commands.

**Acceptance Criteria:**
- Given a clean static checkout served beneath a nested path, when the entry point loads, then all local assets resolve and the meaningful title, edition, attribution, and repository navigation remain present without CSS or JavaScript.
- Given desktop or mobile input, when a player configures PvP or either PvC difficulty, then they can complete roll, capture, placement/pass, win, restart, and confirmed quit flows without a network request.
- Given keyboard-only use, when Tab, Shift+Tab, arrows, Enter, Space, and Escape are used, then every available action has parity, focus is visible/logical, and state changes have semantic names and live announcements.
- Given rudimentary or advanced AI on any valid tested state, when it acts, then it returns a legal move or no move without mutating its input, hanging the page, or exceeding its one/five-second budget.

## Spec Change Log

## Design Notes

Use pure engine transitions over cloned snapshots so simulations cannot corrupt the live game. Treat AI rolling as the computer player's initiation of its own turn; only human turns require the visible Roll action. Use relative `./` asset references and no generated bundle so the deployed directory remains directly inspectable.

## Verification

**Commands:**
- `npm test` -- all engine, AI, static-contract, and DOM tests pass.
- `npm run check` -- JavaScript syntax and static asset/subpath checks pass.
- `python3 -m http.server --directory site` -- the complete game loads and plays from a static server.

**Manual checks (if no CLI):**
- Exercise full PvP and both PvC modes at desktop/mobile widths, including keyboard play, no-legal-play acknowledgment, victory, restart, and both quit-confirmation outcomes.

## Suggested Review Order

**Browser experience**

- Start with the resilient shell, setup choices, play regions, and accessible controls.
  [`index.html:16`](../../site/index.html#L16)

- Review state-driven rendering, perspective labels, keyboard behavior, and live announcements.
  [`app.js:10`](../../site/js/app.js#L10)

- Follow the asynchronous AI turn lifecycle and stale-session cancellation boundary.
  [`app.js:22`](../../site/js/app.js#L22)

- Inspect responsive, non-color-only board states and high-contrast focus treatments.
  [`styles.css:1`](../../site/styles.css#L1)

**Rules and computer play**

- Verify authoritative initialization and player-relative dice coordinate conversion.
  [`game-engine.js:11`](../../site/js/game-engine.js#L11)

- Trace capture resolution, legal destinations, placement, explicit pass, and victory.
  [`game-engine.js:33`](../../site/js/game-engine.js#L33)

- Review random selection and bounded strategic evaluation across all roll outcomes.
  [`ai.js:5`](../../site/js/ai.js#L5)

**Verification and documentation**

- Inspect deterministic rule invariants, edge cases, pass behavior, and victory coverage.
  [`engine.test.js:5`](../../site/tests/engine.test.js#L5)

- Check AI legality, non-mutation, outcome coverage, and timeout boundaries.
  [`ai.test.js:6`](../../site/tests/ai.test.js#L6)

- Confirm the published-game link, edition status, and development commands.
  [`README.md:5`](../../README.md#L5)
