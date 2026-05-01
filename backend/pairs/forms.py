from django import forms


class PaarErstellenForm(forms.Form):
    setup_kinder = forms.BooleanField(
        required=False,
        label="Wir haben Kinder (Kinderbetreuung einbeziehen)",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    setup_haustiere = forms.BooleanField(
        required=False,
        label="Wir haben Haustiere (Haustierpflege einbeziehen)",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class BeitretenForm(forms.Form):
    invite_code = forms.UUIDField(
        label="Einladecode",
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            }
        ),
    )
