from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrierungForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Benutzername"
        self.fields["email"].label = "E-Mail (optional)"
        self.fields["password1"].label = "Passwort"
        self.fields["password2"].label = "Passwort bestätigen"
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
