from django.shortcuts import render
from userprofiles.models import Notification

# Create your views here.

def home(request):
    try:
        updates = Notification.objects.filter(user=request.user)
        unread_updates = updates.filter(is_read=False)
        return render(request, 'index.html', {'notifications': unread_updates})
    except:
        return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')