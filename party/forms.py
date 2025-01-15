import datetime
from django import forms
from django.urls import reverse_lazy

from .models import Party


class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ("party_date", "party_time", "venue", "invitation")
        widgets = {
            "party_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "hx-get": reverse_lazy("partial_check_party_date"),
                    "hx-trigger": "blur",
                    "hx-swap": "outerHTML",
                    "hx-target": "#div_id_party_date",
                }
            ),
            "party_time": forms.TimeInput(attrs={"type": "time"}),
            "invitation": forms.Textarea(
                attrs={
                    # "class": "w-full"
                    "rows": 10,
                    "cols": 30,
                    "hx-get": reverse_lazy("partial_check_invitation"),
                    "hx-trigger": "blur",
                    "hx-swap": "outerHTML",
                    "hx-target": "#div_id_invitation",
                }
            ),
        }

    def clean_invitation(self):
        invitation = self.cleaned_data["invitation"]

        if len(invitation) < 10:
            raise forms.ValidationError("You really should write an invitation.")

        return invitation

    def clean_party_date(self):
        party_date = self.cleaned_data["party_date"]

        if datetime.date.today() > party_date:
            raise forms.ValidationError("You chose a date in the past.")

        return party_date
