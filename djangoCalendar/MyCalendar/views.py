import json
from datetime import datetime, timedelta

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView

from MyCalendar.forms import EventForm, CategoryForm, TaskForm, ProjectForm
from MyCalendar.models import Event, Calendar, Project
from .models import Task


# from .forms import LoginForm  # Pamiętaj o dostosowaniu ścieżki do formularza logowania
class LoginForm(AuthenticationForm):
    pass
def get_json(events):

    return json.dumps(events)


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


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


@login_required(login_url='login')
def dashboard_view(request):
    template_name = 'calendar.html'
    events = Event.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)

    project_events = [
        {
            'title': project.title,
            'start': project.start_date.isoformat() + ' ' + '00:00',
            'end': project.end_date.isoformat() + ' ' + '00:00',
            'color': '#00FF00',  # Kolor zielony
        }
        for project in projects
    ]

    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.start_date.isoformat() + ' ' + event.start_time.strftime('%H:%M'),
            'end': event.end_date.isoformat() + ' ' + event.end_time.strftime('%H:%M'),
            'color': event.calendar.color,
        })

    # Połącz wydarzenia i projekty w jedną listę
    all_events = event_list + project_events
    context = {'object_list': all_events, 'events_json': get_json(all_events)}
    return render(request, template_name, context)

def logout_view(request):
    logout(request)
    return redirect('login')

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.user, request.POST)  # Pass the current user to the form
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            messages.success(request, 'Event added successfully.')
            return redirect('events')
        else:
            messages.error(request, 'Invalid form submission. Please check the form for errors.')
    else:
        form = EventForm(user=request.user)  # Pass the current user to the form

    return render(request, 'add_event.html', {'form': form})


def events_view(request):
    template_name = 'events.html'
    now = timezone.now()

    events = Event.objects.filter(user=request.user)
    context = {'object_list': events}

    return render(request, template_name, context)


class EditEventView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'edit_event.html'
    success_url = reverse_lazy('events')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
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
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'category_form': form})

class EditCategoryView(UpdateView):
    model = Calendar
    form_class = CategoryForm
    template_name = 'edit_category.html'
    success_url = reverse_lazy('category_list')

def task_list_view(request):
    high_priority_tasks = Task.objects.filter(priority=Task.HIGH_PRIORITY, completed=False, user=request.user).order_by(
        'start_date')
    medium_priority_tasks = Task.objects.filter(priority=Task.MEDIUM_PRIORITY, completed=False,
                                                user=request.user).order_by('start_date')
    low_priority_tasks = Task.objects.filter(priority=Task.LOW_PRIORITY, completed=False, user=request.user).order_by(
        'start_date')

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
    completed_tasks = Task.objects.filter(completed=True, user=request.user).order_by('-start_date')

    return render(request, 'completed_tasks.html', {
        'completed_tasks': completed_tasks,
    })

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return HttpResponseRedirect(reverse('task_list'))

class DeleteTaskView(DeleteView):
    model = Task
    template_name = 'delete_task.html'  # Stwórz ten szablon
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

def projects_view(request):
    projects = Project.objects.filter(user=request.user, completed=False)

    return render(request, 'projects.html', {'projects': projects})

def completed_projects_view(request):
    completed_projects = Project.objects.filter(completed=True, user=request.user)
    return render(request, 'completed_projects.html', {'completed_projects': completed_projects})

def add_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('projects')
    else:
        form = ProjectForm()

    return render(request, 'add_project.html', {'form': form})

def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {'form': form})

def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.completed = True
    project.save()
    return HttpResponseRedirect(reverse('projects'))

class DeleteProjectView(DeleteView):
    model = Project
    template_name = 'delete_project.html'
    success_url = reverse_lazy('projects')

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)