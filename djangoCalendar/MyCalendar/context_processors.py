from .models import Project
from django.utils import timezone
from datetime import timedelta

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

    return {'global_notifications': notifications}
