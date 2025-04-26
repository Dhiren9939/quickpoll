from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Poll, Choice


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["question", "expire_date"]
        widgets = {
            "expire_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_expire_date(self):
        expire_date = self.cleaned_data.get("expire_date")
        if expire_date and expire_date <= timezone.now():
            raise forms.ValidationError("Expiration date must be in the future!")
        return expire_date


ChoiceFormSet = inlineformset_factory(
    Poll, Choice, fields=("choice_text",), extra=0, can_delete=True
)
