---
title: 'Fix npm HTTP proxy warning'
type: 'chore'
created: '2026-07-25'
status: 'done'
route: 'one-shot'
---

# Fix npm HTTP proxy warning

## Intent

**Problem:** npm 11 reports that the inherited `npm_config_http_proxy` environment variable is an unknown configuration key, creating noise and warning of a future incompatibility.

**Approach:** Document how to diagnose and remove only the invalid environment variable while retaining valid proxy configuration and identifying its persistent source.

## Suggested Review Order

**Environment remediation**

- Diagnose the inherited variable and safely remove the unsupported npm alias.
  [`README.md:29`](../../README.md#L29)

