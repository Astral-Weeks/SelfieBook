from django.db import models
from django.contrib.auth.models import User


# class PrivacySettings(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     publicaccount = models.BooleanField(default=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, default="SelfieBook")
    birthday = models.DateField(null=True)
    publicaccount = models.BooleanField(default=True)
    profilepicture = models.ImageField(upload_to="/media/", default="staticfiles/img/unknown-user.png")
    # privacysettings = models.ForeignKey(PrivacySettings, on_delete=models.CASCADE)

    def __str__(self):
        return "Username: " + self.user.username + ";   Name: " + self.first_name + " " + self.last_name

class Selfies(models.Model):
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    selfie = models.ImageField(upload_to='images/')
    date = models.DateField()
    caption = models.CharField(default="No caption", max_length=255)


class FriendJunctionTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user.username


class FriendRequestJunctionTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class NotifierJunctionTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FriendRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requester = models.ForeignKey(FriendRequestJunctionTable, on_delete=models.CASCADE)


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(FriendJunctionTable, on_delete=models.CASCADE)
    friendstatus = models.BooleanField(default=False)

    def __str__(self):
        return "Users: " + self.user.username + " & " + self.friend.user.username

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifier = models.ForeignKey(NotifierJunctionTable, on_delete=models.CASCADE)

class FriendPhotoNotification(models.Model):
    selfie = models.ForeignKey(Selfies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    # notifier = models.ForeignKey(NotifierJunctionTable, on_delete=models.CASCADE)
