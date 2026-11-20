from .models import Notification

def notification_context(request):
    """Provides unread notifications and count across all templates."""
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by('-created_at')[:5]
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return {
            'unread_notifications': unread_notifications,
            'unread_notification_count': unread_count,
            'PROJECT_NAME': 'AI College Placement Management System',
            'PROJECT_TAGLINE': 'Your Career Starts Here.',
        }
    return {
        'unread_notifications': [],
        'unread_notification_count': 0,
        'PROJECT_NAME': 'AI College Placement Management System',
        'PROJECT_TAGLINE': 'Your Career Starts Here.',
    }
