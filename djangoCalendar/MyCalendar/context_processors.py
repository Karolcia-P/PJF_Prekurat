from .models import Project, Event
from django.utils import timezone
from datetime import timedelta, datetime
import time


def global_notifications(request):
    notifications = []

    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user, completed=False)
        current_datetime = timezone.now()

        for project in projects:
            if project.end_date and current_datetime <= project.end_date <= current_datetime + timedelta(days=1):
                notification = {
                    'title': 'Project is ending soon.',
                    'content': f'Title: {project.title} <br> End Date: {project.end_date.strftime("%B %d, %Y")}',
                }
                notifications.append(notification)

        events = Event.objects.filter(user=request.user, end_date__gte=timezone.now(), start_date__gte=timezone.now())

        for event in events:
            # Utwórz obiekt timedelta na podstawie atrybutów notification
            notification_timedelta = timedelta(hours=event.notification.hour, minutes=event.notification.minute)

            # Oblicz notification_time odejmując notification_timedelta od start_datetime
            start_datetime = datetime.combine(event.start_date, event.start_time)
            notification_time = start_datetime - notification_timedelta
            system_localtime = time.localtime()
            system_datetime = datetime.fromtimestamp(time.mktime(system_localtime))
            current_datetime_naive = system_datetime
            if notification_time <= current_datetime_naive <= start_datetime:
                notification = {
                    'title': 'Event Reminder.',
                    'content': f'Title: {event.title} <br> Start: {event.start_date.strftime("%B %d, %Y")}, {event.start_time.strftime("%H:%M")}',
                }

                if notification not in notifications:
                    notifications.append(notification)

    return {'global_notifications': notifications}