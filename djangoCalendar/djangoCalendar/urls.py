"""
URL configuration for djangoCalendar project.

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
from django.contrib.auth.decorators import login_required
from django.urls import path

from MyCalendar.views import login_view, SignUpView, dashboard_view, logout_view, events_view, add_event, category_list, \
    add_category, EditCategoryView, EditEventView, DeleteEventView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/', login_required(dashboard_view), name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('events/', events_view, name='events'),
    path('add_event/', add_event, name='add_event'),
    path('edit_event/<int:pk>/', EditEventView.as_view(), name='edit_event'),
    path('events/delete/<int:pk>/', DeleteEventView.as_view(), name='delete_event'),
    path('category/', category_list, name='category_list'),
    path('add_category/', add_category, name='add_category'),
    path('edit_category/<int:pk>/', EditCategoryView.as_view(), name='edit_category'),
]
