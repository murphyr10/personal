from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        # Fetch unread notifications for the logged-in user
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        
        return {
            'unread_notifications': unread_notifications,  # Unread notifications for badge
            'all_notifications': all_notifications,  # All notifications to show in dropdown
        }
    return {}