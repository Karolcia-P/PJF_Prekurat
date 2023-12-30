"""
URL configuration for calendarProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Calendar.views import login_view, register_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('user_dashboard/', dashboard_view, name='dashboard'),
]
