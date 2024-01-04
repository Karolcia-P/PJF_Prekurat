from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Event, Calendar, Task


class EventForm(forms.ModelForm):
    calendar = forms.ModelChoiceField(
        queryset=Calendar.objects.all(),
        label='Kalendarz',  # Etykieta pola
        widget=forms.Select(attrs={'class': 'form-control'}),  # Dodatkowe atrybuty dla widgetu
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'calendar', 'notification']
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, user, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['calendar'].queryset = Calendar.objects.filter(user=user)

        if instance:
            self.fields['start_date'].initial = instance.start_date
            self.fields['end_date'].initial = instance.end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise ValidationError("End date must be later than start date.")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['name', 'color']


class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'priority']

