# Strategic Reserve — HTML edition

This directory is the directly deployable, dependency-free browser edition of **Strategic Reserve**, a game by Mark Steere. The existing GitHub Pages workflow publishes this directory as-is; there is no compilation step, backend, CDN, or network request.

## Play and controls

Choose two local players or play Red against the rudimentary/advanced Blue computer, then select **Start game**. The active human explicitly selects **Roll Dice**, then chooses a highlighted legal square. If none exists, the game explains the situation and presents **Pass — No Legal Play** for acknowledgment.

- **Pointer:** select any enabled control or highlighted board square.
- **Keyboard:** use Tab/Shift+Tab between controls, arrow keys within the board, Enter or Space to place, and Escape to dismiss the quit confirmation.
- **Restart/quit:** **New Game** resets with the same configuration. **Quit Game** asks for confirmation before returning to setup.

## Static layout

- `index.html` — semantic game and setup shell
- `styles.css` — responsive and accessible visual presentation
- `js/game-engine.js` — authoritative pure rules/state transitions
- `js/ai.js` — non-mutating computer move selectors
- `js/app.js` — rendering, input, announcements, and AI scheduling
- `tests/` — dependency-free Node test suite and static checks

Run `npm test` and `npm run check` from the repository root. For manual play, run `python3 -m http.server 8000 --directory site`, then open `http://localhost:8000/`.

The dependency-free Node suite exercises the engine and AI behavior and checks controller accessibility contracts. Node does not provide a browser DOM, focus model, or native `<dialog>` implementation, so actual focus movement, modal behavior, and delayed-callback cancellation are manual browser checks rather than misleading fake-DOM tests. Verify those flows in both PvP and PvC while performing the manual play check above.
