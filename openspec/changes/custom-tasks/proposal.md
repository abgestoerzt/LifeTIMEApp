# Custom Tasks

## What

Let both partners add their own tasks to the survey — tasks that matter to their specific household but aren't in the standard catalog. Custom tasks appear in the survey, the redistribution plan, and weekly check-ins exactly like standard tasks.

## Why

The standard catalog covers ~45 common tasks, but every couple has a unique household. A couple with a vegetable garden, a rental property, or a family business has tasks that don't exist in the catalog. Without this, the app gives an incomplete picture.

The data model already supports custom tasks (`Aufgabe.ist_standard=False`, `Aufgabe.paar_session` FK). This change adds the missing UI and service layer.

## Scope

**In scope:**
- Both partners can add a custom task at any time while `PaarSession.status ∈ {offen, test_laeuft}`
- Custom tasks belong to a couple's session (not global)
- Custom tasks go into a fixed "Eigene Aufgaben" category (no category choice needed)
- A partner can delete a custom task they added, but only if it hasn't been answered yet
- Custom tasks appear in survey, plan, and check-ins

**Out of scope:**
- Editing a task's name after creation
- Reordering custom tasks
- Sharing custom tasks across sessions
- Custom categories (only the fixed "Eigene Aufgaben" bucket)
