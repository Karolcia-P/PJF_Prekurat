from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from MyCalendar.forms import EventForm
from MyCalendar.models import Event


# from .forms import LoginForm  # Pamiętaj o dostosowaniu ścieżki do formularza logowania
class LoginForm(AuthenticationForm):
    pass

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
    return render(request, 'calendar.html')

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
            return redirect('dashboard')
    else:
        form = EventForm()

    return render(request, 'add_event.html', {'form': form})


@login_required(login_url='login')
def events_view(request):
    template_name = 'events.html'

    # Pobierz dzisiejszą datę i czas
    now = datetime.now()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            return redirect('events')
    else:
        form = EventForm()

    # Pobierz tylko aktualne wydarzenia użytkownika
    events = Event.objects.filter(user=request.user, end_date__gte=now)

    context = {'form': form, 'events': events}

    return render(request, template_name, context)