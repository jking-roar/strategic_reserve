# Browser Edition Notes

Last reviewed: 2026-07-26

## Scope in repository

The browser edition is implemented in `site/` as a static, dependency-free runtime artifact.

## Structure

- `site/index.html` - semantic application shell and controls.
- `site/styles.css` - responsive and accessible presentation.
- `site/js/game-engine.js` - browser rules authority.
- `site/js/ai.js` - rudimentary and advanced AI move selection.
- `site/js/app.js` - interaction flow, rendering, and announcements.
- `site/tests/` - Node test and static contract checks.

## Commands (run from repo root)

```bash
npm test
npm run check
python -m http.server 8000 --directory site
```

Open `http://localhost:8000/` for manual play checks.

See the [browser controls and manual test notes](../../site/README.md) for player
instructions, keyboard behavior, and current limitations.
