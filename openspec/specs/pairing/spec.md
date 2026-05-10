# Spec: Pairing

## Capability

Two users form a "Paar" (couple) by one creating a session and sharing an invite code with the other. The session then tracks all shared state (test, plan, check-ins) for the couple.

## Implementation

- `pairs/models.py`: `PaarSession`
- `pairs/services.py`: `paar_erstellen`, `paar_beitreten`, `get_aktive_session`
- `pairs/views.py`: `erstellen`, `einladung`, `beitreten`
- `pairs/forms.py`: `PaarErstellenForm`, `BeitretenForm`

## Data model

```
PaarSession
├─ partner_a (FK User)              — creator
├─ partner_b (FK User, nullable)    — null until invited partner joins
├─ invite_code (UUIDField, unique)  — generated on creation
├─ invite_expires_at (DateTimeField)— 7 days from creation
├─ status (CharField)               — see Status lifecycle below
├─ setup_kinder (BooleanField)      — activates Kinderbetreuung category
├─ setup_haustiere (BooleanField)   — activates Haustiere category
└─ created_at (DateTimeField)
```

## Status lifecycle

```
offen
  → test_laeuft   (when partner_b joins via invite code)
  → beide_fertig  (when both partners complete the survey)
  → plan_aktiv    (when both partners sign the redistribution plan)
```

Status only moves forward. No rollback.

## URLs

| URL | Name | Description |
|---|---|---|
| `/paar/erstellen/` | `pairs:erstellen` | Create pair + choose optional categories |
| `/paar/einladung/<pk>/` | `pairs:einladung` | Show invite code (partner_a only) |
| `/paar/beitreten/` | `pairs:beitreten` | Enter invite code (partner_b) |

## Behavior

### Creating a pair (`paar_erstellen`)
- Only partner_a creates the session
- A UUID invite code is generated and stored
- Invite expires 7 days from creation
- `PaarErstellenForm` has checkboxes for `setup_kinder` and `setup_haustiere`
- On success: redirects to `pairs:einladung`

### Invite code page
- Shows the UUID code for partner_a to share (copy/paste, no email sending)
- Shows expiry date
- Only accessible to partner_a of the session

### Joining (`paar_beitreten`)
- Partner_b enters the UUID code in `BeitretenForm`
- Validation: code must exist, not expired, not already used (partner_b not set), user must not be partner_a
- On success: sets `partner_b`, status → `test_laeuft`, redirects to `/test/`

### Active session resolution
- `get_aktive_session(user)` returns the most recent `PaarSession` where user is partner_a or partner_b
- Returns `None` if no session exists
- Used by dashboard and all downstream views to find the current session

## Constraints

- A user can be partner_a of multiple sessions (e.g. after retrying) but `get_aktive_session` returns only the most recent
- Invite code is single-use (once partner_b is set, code cannot be reused)
- No mechanism to leave or delete a session in v1
