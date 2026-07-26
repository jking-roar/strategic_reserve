# Python Desktop Release Checklist

This is the release coverage map for Epic 6. A release passes only when every
automated gate and every applicable manual row passes with **zero critical
defects**. Record the OS, Python/Tk versions, screen reader, artifact name, and
date with the release evidence.

## Automated gates

| Contract | Evidence |
| --- | --- |
| Arrow boundaries, Enter/Space parity, Escape cancellation, state descriptions | `python -m pytest -q python/tests/test_ui.py` |
| Engine authority, all dice/capture outcomes, terminal lock | `python -m pytest -q python/tests/test_rules.py` |
| Rudimentary under 1 second; advanced bounded under 5 seconds | `python -m pytest -q python/tests/test_ai.py` |
| UI dependency direction and import safety | `python -m pytest -q python/tests/test_architecture.py` |
| Build and clean install | `python -m build python/`; install the named wheel from `python/dist/` in a fresh venv (do not use a shell wildcard on Windows) |
| Installed launch | `xvfb-run -a sh -c 'strategic-reserve & pid=$!; sleep 2; kill $pid'` |

## Contrast evidence

Ratios use WCAG relative luminance. Essential non-text indicators require at
least 3:1 against adjacent colors; text requires 4.5:1. Solid checker shapes,
borders, letters/dashes, and spacing ensure that color is never the only cue.

| State / adjacent colors | Ratio | Result |
| --- | ---: | --- |
| Normal grid `#333333` / beige `#F5F5DC` | 11.42:1 | Pass |
| Legal border `#006400` / legal fill `#90EE90` | 5.25:1 | Pass |
| Target border/marker outline `#765400` / gold marker `#FFD700` | 4.93:1 | Pass |
| Target dashed border `#765400` / beige normal cell | 6.25:1 | Pass |
| Target dashed border `#765400` / green legal cell | 4.88:1 | Pass |
| Focus/hover `#C24100` / beige | 4.69:1 | Pass |
| Focus/hover `#C24100` / legal fill | 3.66:1 | Pass |
| Focus/hover `#C24100` / gold target marker | 3.70:1 | Pass |
| Disabled border `#767676` / beige | 4.10:1 | Pass |

The focus border (2px inset), target border (6px inset), gold target marker
(20px inset), and disabled dash (10px inset) are spatially separated when
overlapping. Legal borders remain rendered on disabled squares, so disabling the
board does not erase the legal non-color cue.

Recalculate after any palette change. Inspect normal, hover, keyboard focus,
legal, target, focus+legal, focus+target, disabled, and terminal states at 100%
and 200% scaling; cues must remain distinct and un-clipped.

## Manual supported-desktop matrix

Run on Windows 10/11 with Narrator or NVDA, macOS 13+ with VoiceOver, and a
current Linux desktop with a Python build containing Tk 8.6 and Orca where
available.

- [ ] Fresh environment installs the wheel without fetching an undeclared
  runtime dependency; `strategic-reserve` opens. A missing Tk/display produces
  an actionable terminal error rather than an unexplained import traceback.
- [ ] Tab and Shift+Tab follow the visible board/control order. Arrows wrap
  predictably; Enter and Space match click; Escape dismisses transient square
  description without changing state and answers
  No in the quit dialog without changing game state.
- [ ] Pointer hover and keyboard focus show a 3px dark-orange (`#C24100`) cue only on the active
  square. Legal border, target dashed border/`T`, disabled treatment, and focus
  remain distinguishable when overlapping.
- [ ] The screen reader exposes the named game status and reads updated turn,
  purple/green dice, target row/column, legal count, captures, reserves, invalid
  actions, pass, and winner. Verify these same facts are visible.
- [ ] Complete PvP, rudimentary PvC, and advanced PvC games through start, every
  capture category, placement, no-move pass, win, New Game/restart, and confirmed
  quit. No terminal board action is accepted and no stale AI result changes a
  restarted/closed session.
- [ ] Inspect source distribution, wheel metadata, and documentation for Mark
  Steere attribution, controls, commands, supported environment, and limitations.

## Known limitations

Accessibility exposure depends on the operating system's Tk bridge. Screen-reader
  behavior therefore has a repeatable per-desktop release gate; release records
  capture results rather than this implementation checklist claiming an unrun signoff. The game is
local, desktop-only, and intentionally has no save/load, network play, mobile UI,
audio, tutorial, replay, themes, or custom board sizes.
