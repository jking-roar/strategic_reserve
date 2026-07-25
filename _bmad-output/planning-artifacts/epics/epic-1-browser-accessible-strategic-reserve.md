---
epic: 1
title: Browser-Accessible Strategic Reserve
status: done
source: _bmad-output/planning-artifacts/epics.md
lastReviewed: 2026-07-25
---

# Epic 1: Browser-Accessible Strategic Reserve

Visitors can discover Strategic Reserve through GitHub Pages and play a complete, accessible HTML edition before or independently of the Python desktop release.

## Story Status

- 1.1 - Done
- 1.2 - Done
- 1.3 - Done
- 1.4 - Done
- 1.5 - Done

## Stories

### Story 1.1: Publish the Project Site

As a visitor, I want a reliable project page and a direct link from the repository, so that I can find and open Strategic Reserve in a browser.

**Acceptance Criteria:**

**Given** the repository's default branch, **when** the Pages deployment workflow completes, **then** it publishes a static entry point using only repository-hosted assets and no server-side runtime.

**Given** the site is hosted below a GitHub Pages project path, **when** any published page or asset is requested, **then** its URL resolves without assuming domain-root hosting.

**Given** a visitor reads the README, **when** they look for a playable version, **then** a prominent link opens the published site and the README distinguishes the HTML and Python/Tkinter editions.

### Story 1.2: Explore the Browser Game Shell

As a browser player, I want a responsive game shell, so that I can understand the game and its available modes on desktop or mobile.

**Acceptance Criteria:**

**Given** the published entry point, **when** it loads at a supported viewport, **then** it presents the game title, mode and difficulty controls, New Game, the 6x6 board region, dice region, reserve counters, status text, and project attribution.

**Given** keyboard-only navigation, **when** the player uses Tab, Shift+Tab, arrow keys, Enter, Space, or Escape, **then** focus is visible, follows a logical order, and every available shell control has pointer-equivalent operation.

**Given** CSS or JavaScript assets fail to load, **when** the document renders, **then** meaningful title, edition status, and repository navigation remain available as HTML content.

### Story 1.3: Play a Complete Local Browser Game

As two local players, I want the HTML edition to enforce the official rules, so that we can finish a valid game entirely in the browser.

**Acceptance Criteria:**

**Given** a new browser game, **when** play begins, **then** the official initial board, reserves, starting player, and two fair six-sided dice are represented in browser-owned state.

**Given** any empty, friendly-group, or enemy-group target, **when** a roll resolves, **then** group discovery, captures, legal placements, reserve updates, and turn advancement match FR-5 through FR-9 without a network request.

**Given** legal destinations and the rolled target, **when** they render, **then** they use distinct accessible labels and the specified legal, target, hover, and focus treatments without relying on color alone.

**Given** a player places their final reserve checker, **when** the placement completes, **then** the winner is announced immediately, further board input is disabled, and a New Game action is available.

### Story 1.4: Play Against Browser AI

As a solo browser player, I want selectable computer opponents, so that I can practice at an appropriate difficulty without installing Python.

**Acceptance Criteria:**

**Given** player-versus-computer mode, **when** rudimentary difficulty is selected, **then** the AI chooses a legal move randomly and completes within one second under documented test conditions.

**Given** advanced difficulty, **when** the AI selects a move, **then** it considers all 36 next-roll outcomes, returns a best-so-far legal move within five seconds, and does not freeze browser input indefinitely.

**Given** any valid sparse, full, capture-heavy, no-move, or near-win state, **when** either browser AI acts, **then** it returns a legal move or no move without corrupting game state.

### Story 1.5: Validate the Static Browser Release

As a browser player, I want a stable and accessible published game, so that I can play from common devices without installation.

**Acceptance Criteria:**

**Given** the production Pages artifact, **when** automated checks load it from a non-root base path, **then** internal navigation and all required HTML, CSS, JavaScript, and media assets succeed without server rewrites.

**Given** supported desktop and mobile browser sizes, **when** a full PvP game and both PvC difficulties are exercised, **then** setup, roll, capture, placement, win, restart, and responsive layout complete with no critical defect.

**Given** an accessibility audit and keyboard playthrough, **when** menus, board states, status changes, and dialogs are evaluated, **then** semantic names, announcements, keyboard parity, focus visibility, and WCAG AA contrast meet the UX contract.

