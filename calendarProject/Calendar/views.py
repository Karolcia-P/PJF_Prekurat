# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from schedule.models import Calendar


class LoginForm(AuthenticationForm):
    pass

class CalendarView(View):
    template_name = 'calendar_view.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'calendar_list': Calendar.objects.all()})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

def calendar_view(request):
    return render(request, 'calendar.html')

def add_event_view(request):
    # Dodaj kod obsługujący formularz dodawania wydarzeń
    return render(request, 'add_event.html')

def task_list_view(request):
    # Dodaj kod obsługujący listę zadań
    return render(request, 'task_list.html')

def current_projects_view(request):
    # Dodaj kod obsługujący zakładkę z aktualnymi projektami
    return render(request, 'current_projects.html')