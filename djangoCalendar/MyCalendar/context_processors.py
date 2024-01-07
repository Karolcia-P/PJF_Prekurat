from .models import Project, Event
from django.utils import timezone
from datetime import timedelta, datetime


def global_notifications(request):
    notifications = []

    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user, completed=False)
        current_date = timezone.now().date()
        for project in projects:
            if project.end_date and current_date <= project.end_date <= current_date + timedelta(days=1):
                notification = {
                    'title': 'Project is ending soon.',
                    'content': f'Title: {project.title} <br> End Date: {project.end_date.strftime("%B %d, %Y")}',
                }
                notifications.append(notification)

        events = Event.objects.filter(user=request.user, end_date__gte=timezone.now(), start_date__gte=timezone.now())

        for event in events:
            # Utwórz obiekt timedelta na podstawie atrybutów notification
            notification_timedelta = timedelta(hours=event.notification.hour, minutes=event.notification.minute)

            # Oblicz notification_time odejmując notification_timedelta od start_date
            notification_time = event.start_date - notification_timedelta

            if timezone.now() >= notification_time and event.start_date >= timezone.now():
                notification = {
                    'title': 'Event Reminder.',
                    'content': f'Title: {event.title} <br> Start Date: {event.start_date.strftime("%B %d, %Y %H:%M")}',
                }

                if notification not in notifications:
                    notifications.append(notification)

    return {'global_notifications': notifications}
