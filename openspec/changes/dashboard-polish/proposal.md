# Dashboard Polish

## What

Turn the current empty dashboard shell into a useful hub that tells each user exactly where they are in the flow and what to do next. Also polish the landing page for logged-out visitors.

## Why

The dashboard view currently passes `paar_session` to a template but does almost nothing with it. Per the Konzept (section 7): the dashboard is the *only* reminder mechanism for check-ins — there's no email. That means it needs to be clear, actionable, and specific about the check-in state.

## Scope

**In scope:**
- Dashboard states per `PaarSession.status` (or no session)
- Check-in state: "ausstehend" / "Partner:in steht noch aus" / "beide fertig" / "vor X Tagen"
- Next-action CTA per flow step
- Landing page: a real public homepage for logged-out users

**Out of scope:**
- Notifications / push
- Email reminders
- Activity history beyond check-in timing
