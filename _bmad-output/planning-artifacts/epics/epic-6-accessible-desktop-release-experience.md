---
epic: 6
title: Accessible Desktop Release Experience
status: not-started
source: _bmad-output/planning-artifacts/epics.md
lastReviewed: 2026-07-25
---

# Epic 6: Accessible Desktop Release Experience

Keyboard and assistive-technology users can complete every journey, and the packaged application meets the visual and quality contract.

## Story Status

- 6.1 - Not started
- 6.2 - Not started
- 6.3 - Not started

## Stories

### Story 6.1: Play the Board Entirely by Keyboard

As a keyboard user, I want parity with pointer interaction, so that I can complete a game without a mouse.

**Acceptance Criteria:**

**Given** board focus, **when** arrow keys are pressed, **then** focus moves predictably within the grid; Enter or Space activates a legal square.

**Given** any surface, **when** Tab and Shift+Tab are used, **then** focus follows visual order; Escape cancels selection or closes a non-destructive dialog.

**Given** pointer or keyboard focus, **when** a board square is targeted, **then** the orange outline is visible and distinguishable from target and legal-move states.

### Story 6.2: Announce State and Meet Contrast Standards

As an assistive-technology user, I want state changes announced and visible, so that I receive equivalent gameplay information.

**Acceptance Criteria:**

**Given** turn, roll, capture, reserve, invalid-action, or winner changes, **when** they occur, **then** concise accessible text communicates the change without relying only on color.

**Given** every normal, hover, focus, legal, target, and disabled state, **when** audited, **then** text and essential indicators meet WCAG AA contrast and visible-focus requirements.

### Story 6.3: Validate the Release Journey

As a player, I want a stable distributable game, so that installation and complete play work on a supported desktop.

**Acceptance Criteria:**

**Given** a clean supported Python environment, **when** documented launch instructions are followed, **then** the application opens without undeclared dependencies.

**Given** automated and manual release checks, **when** PvP and both PvC difficulties are played through start, captures, win, restart, and quit, **then** all requirements in the coverage map pass with no critical defects.

**Given** the release artifact, **when** source and documentation are inspected, **then** game attribution, controls, test commands, supported environment, and known limitations are present.

