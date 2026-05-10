from django import forms


class AufgabeErstellenForm(forms.Form):
    bezeichnung = forms.CharField(
        max_length=200,
        label="Aufgabe",
        strip=True,
        widget=forms.TextInput(attrs={"placeholder": "z.B. Gemüsegarten pflegen"}),
    )
