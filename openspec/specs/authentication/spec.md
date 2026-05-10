# Spec: Authentication

## Capability

Users can register, log in, and log out. Authentication is required for all app functionality beyond the landing page.

## Implementation

- `accounts/views.py`: `registrieren` view + Django's built-in `LoginView` and `LogoutView`
- `accounts/forms.py`: `RegistrierungForm` (extends `UserCreationForm`, German labels, Bootstrap styling)
- Django's built-in `User` model — no custom user model

## URLs

| URL | Name | Description |
|---|---|---|
| `/registrieren/` | `accounts:registrieren` | Registration form (GET + POST) |
| `/login/` | `accounts:login` | Login form (GET + POST) |
| `/logout/` | `accounts:logout` | Logout (POST) |

## Behavior

### Registration
- Fields: username, password1, password2
- On success: logs user in automatically, redirects to `/dashboard/`
- On failure: re-renders form with errors

### Login
- Standard Django `LoginView`
- On success: redirects to `settings.LOGIN_REDIRECT_URL` (→ `/dashboard/`)
- Unauthenticated requests to protected pages are redirected to `/login/?next=<url>`

### Logout
- POST only (CSRF protected)
- Redirects to `/` (landing page)

## Access control

All views except `/`, `/login/`, `/registrieren/` require authentication via `@login_required` or `LoginRequiredMixin`. The `LOGIN_URL` setting points to `/login/`.

## Data model

Uses Django's built-in `User` model directly. No profile extension. Relevant fields: `username`, `password` (hashed), `date_joined`.
