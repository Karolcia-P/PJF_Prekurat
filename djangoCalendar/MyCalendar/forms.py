from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Event, Calendar


class EventForm(forms.ModelForm):
    calendar = forms.ModelChoiceField(queryset=Calendar.objects.all())

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'calendar', 'notification']
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise ValidationError("End date must be later than start date.")

