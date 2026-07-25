# Strategic Reserve

Implementation of **Strategic Reserve** for local and computer play.

## Play in your browser

**[Launch the playable HTML edition](https://jking-roar.github.io/strategic_reserve/)** — a complete, responsive static game with two-player and rudimentary/advanced computer modes. It requires no installation or backend and is published through the repository's GitHub Pages workflow. The [source repository](https://github.com/jking-roar/strategic_reserve) remains available alongside it.

The **HTML edition** in `site/` is playable now. A separate **Python/Tkinter desktop edition** is planned; the browser implementation does not replace it.

Keyboard players can Tab through controls, use arrow keys on the board, and press Enter or Space to place. Every human roll is user-initiated, and a turn with no legal placement waits for explicit acknowledgment.

## Game Attribution

**Strategic Reserve** is a game by **Mark Steere**.

## Game Overview

Strategic Reserve is a two-player board game played on a 6×6 grid, blending tactical positioning with dice-driven events. Each player starts with six checkers in reserve and attempts to be the first to place all reserve checkers onto the board.

On each turn, two dice select a target square (column and row). The result determines what happens next:

- If the square is in an **enemy group**, that entire connected group is removed and returned to the opponent’s reserve.
- If the square is in one of your **own groups**, all orthogonally adjacent enemy groups are removed, and your placement is restricted to an empty square adjacent to that friendly group.
- If the square is **empty**, you may place on any empty square.

Groups are orthogonally connected sets of same-color checkers. Captures can return pieces to reserve, so board control shifts quickly over the course of play.

## Objective

Win by being the first player to empty your reserve.

---

Rules source: `rules.txt`

## Browser edition development

Run `npm test` for the engine, AI, and static accessibility contracts, and `npm run check` for syntax and subpath-safe asset validation. To serve the production artifact locally, run `python3 -m http.server 8000 --directory site`.
