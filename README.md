# Strategic Reserve

Implementation of **Strategic Reserve** for local and computer play.

## Play in your browser

**[Launch the playable HTML edition](https://jking-roar.github.io/strategic_reserve/)** — a complete, responsive static game with two-player and rudimentary/advanced computer modes. It requires no installation or backend and is published through the repository's GitHub Pages workflow. The [source repository](https://github.com/jking-roar/strategic_reserve) remains available alongside it.

The **HTML edition** in `site/` and the **Python/Tkinter desktop edition** are
both playable. The desktop game supports local PvP plus rudimentary and bounded
advanced computer opponents (the computer always plays Blue).

Keyboard players can Tab through controls, use arrow keys on the board, and press Enter or Space to place. Every human roll is user-initiated, and a turn with no legal placement waits for explicit acknowledgment.

## Install the desktop edition

The supported runtime is Python 3.11 or newer with Tk 8.6 on a graphical Windows,
macOS, or Linux desktop. Build and install the distributable entry point with:

```sh
python -m pip install build
python -m build python/
python -m pip install python/dist/strategic_reserve_python-0.1.0-py3-none-any.whl
strategic-reserve
```

Tkinter ships with standard Windows/macOS Python installers; Linux users may
need their distribution's `python3-tk` package. The game has no third-party
runtime dependencies. See [desktop controls and limitations](python/README.md)
and the [release/accessibility checklist](docs/python/release-checklist.md).

## Game Attribution

**Strategic Reserve** is a game by **Mark Steere**.

## Game Overview

Strategic Reserve is a two-player board game played on a 6×6 grid, blending tactical positioning with dice-driven events. Each player starts with six checkers in reserve and attempts to be the first to place all reserve checkers onto the board.

The game also begins with six checkers per player already arranged on the board;
see [`rules.txt`](rules.txt) for the starting position and complete rules.

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

## Development troubleshooting

### npm reports `Unknown env config "http-proxy"`

npm 11 treats `npm_config_http_proxy` as an unknown npm configuration key.
This warning comes from the surrounding development environment, not from this
project (which has no npm configuration). In a POSIX shell, confirm the source
and remove both possible spellings from the current session:

```sh
env | sort | grep -iE '(^|_)(http|https)_proxy='
unset npm_config_http_proxy NPM_CONFIG_HTTP_PROXY
```

Before unsetting the variable, ensure `HTTP_PROXY` and `HTTPS_PROXY` (or their
lowercase equivalents) contain the real proxy URLs if network access requires
them. Do not remove `npm_config_https_proxy`; npm 11 still recognizes it.

If the warning returns in a new shell, remove `npm_config_http_proxy` from the
configuration that launches the process, such as a shell profile, development
container, CI variable, or system environment. In this development container it
is defined in `/etc/environment`; changing that system-wide file requires
administrator access and affects future processes. Adding an `.npmrc` cannot
remove an inherited environment variable.
