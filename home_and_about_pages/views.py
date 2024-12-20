from django.shortcuts import render
from userprofiles.models import Friends, Notification, FriendPhotoNotification

# Create your views here.

def home(request):
    try:
        updates = Notification.objects.filter(user=request.user)
        # photoupdates = FriendPhotoNotification.objects.filter()
        unread_updates = updates.filter(is_read=False)
        # photo updates
        friends = Friends.objects.filter(user=request.user, friendstatus=True)
        empty_queryset = FriendPhotoNotification.objects.none()
        for person in friends:
            if person.friendstatus is True:
                photonotifications = FriendPhotoNotification.objects.filter(user=person.friend.user, is_read=False)
                empty_queryset = empty_queryset | photonotifications
        return render(request, 'index.html', {'notifications': unread_updates, 'photonotifications': empty_queryset})
    except:
        return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')