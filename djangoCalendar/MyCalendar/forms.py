from django import forms
from django.core.exceptions import ValidationError

from .models import Event, Calendar, Task, Project


class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'datetime-local'}))

    calendar = forms.ModelChoiceField(
        queryset=Calendar.objects.none(),  # Set an empty initial queryset
        label='Calendar',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'calendar', 'notification']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['calendar'].queryset = Calendar.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise ValidationError("End date must be later than the start date.")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['name', 'color']


class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'priority']





class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("Start date must be before the end date.")

