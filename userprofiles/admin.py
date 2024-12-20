from django.contrib import admin
from .models import Profile, Selfies, Friends, FriendRequests, FriendJunctionTable, FriendRequestJunctionTable, Notification, FriendPhotoNotification

admin.site.register(Profile)
admin.site.register(Selfies)
admin.site.register(Friends)
admin.site.register(FriendRequests)
admin.site.register(FriendJunctionTable)
admin.site.register(Notification)
admin.site.register(FriendPhotoNotification)

