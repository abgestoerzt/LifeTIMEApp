# Test Coverage

## What

Write a comprehensive test suite for all existing code — services, views, and models with methods — before any new features are added. Target ≥ 80% coverage across all apps.

## Why

The codebase has a full pytest + pytest-django + factory-boy setup ready to go but zero actual tests. Business-critical logic (scoring, perception gap detection, sign-off flows, status transitions) is completely untested. Any new feature built on top of untested code compounds the risk.

## Scope

**In scope:**
- All service functions in: `pairs`, `survey`, `results`, `plan`, `checkins`
- All views: auth guards, status-based access control, redirects, form handling
- Model methods: `Umverteilung.beide_signiert()`, `PaarSession` status transitions
- Shared test factories for all models (via `factory-boy`)

**Out of scope:**
- Template rendering beyond status codes and redirects
- Frontend / JavaScript behavior
- Admin interface

## Success criteria

- `uv run pytest --cov=. --cov-report=term-missing` reports ≥ 80% overall
- All service functions have at least one passing test
- All views have at least one test covering the happy path and one covering access denial
- CI-ready: tests run cleanly with no warnings
