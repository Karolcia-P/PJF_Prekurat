import json
from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView

from MyCalendar.forms import EventForm, CategoryForm, TaskForm
from MyCalendar.models import Event, Calendar
from .models import Task


# from .forms import LoginForm  # Pamiętaj o dostosowaniu ścieżki do formularza logowania
class LoginForm(AuthenticationForm):
    pass
def get_events_json(events):
    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'color': event.calendar.color,
        })
    return json.dumps(event_list)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'
#     success_url = reverse_lazy('dashboard')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


@login_required(login_url='login')
def dashboard_view(request):
    template_name = 'calendar.html'
    now = timezone.now()
    events = Event.objects.filter(user=request.user)
    # calendar_colors = {calendar.id: calendar.color for calendar in Calendar.objects.filter(user=request.user)}
    context = {'object_list': events, 'events_json': get_events_json(events)}
    return render(request, template_name, context)

def logout_view(request):
    logout(request)
    return redirect('login')

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            messages.success(request, 'Event added successfully.')
            return redirect('events')
        else:
            messages.error(request, 'Invalid form submission. Please check the form for errors.')
    else:
        form = EventForm(user=request.user)

    return render(request, 'add_event.html', {'form': form})


def events_view(request):
    template_name = 'events.html'
    now = timezone.now()

    events = Event.objects.filter(user=request.user, end_date__gt=now)
    context = {'object_list': events}

    return render(request, template_name, context)


class EditEventView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'edit_event.html'
    success_url = reverse_lazy('events')

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteEventView(DeleteView):
    model = Event
    success_url = reverse_lazy('events')
    template_name = 'event_confirm_delete.html'
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

def category_list(request):
    categories = Calendar.objects.filter(user=request.user)
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.user = request.user
            new_category.save()
            return redirect('category')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'category_form': form})

class EditCategoryView(UpdateView):
    model = Calendar
    form_class = CategoryForm
    template_name = 'edit_category.html'
    success_url = reverse_lazy('category_list')

def task_list_view(request):
    high_priority_tasks = Task.objects.filter(priority=Task.HIGH_PRIORITY, completed=False).order_by('start_date')
    medium_priority_tasks = Task.objects.filter(priority=Task.MEDIUM_PRIORITY, completed=False).order_by('start_date')
    low_priority_tasks = Task.objects.filter(priority=Task.LOW_PRIORITY, completed=False).order_by('start_date')

    return render(request, 'task_list.html', {
        'high_priority_tasks': high_priority_tasks,
        'medium_priority_tasks': medium_priority_tasks,
        'low_priority_tasks': low_priority_tasks,
    })

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the current user to the task
            task.save()
            return redirect('task_list')  # Adjust this to your actual redirect URL
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})

class EditTaskView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'edit_task.html'
    success_url = reverse_lazy('task_list')

def completed_tasks_view(request):
    completed_tasks = Task.objects.filter(completed=True).order_by('-start_date')

    return render(request, 'completed_tasks.html', {
        'completed_tasks': completed_tasks,
    })