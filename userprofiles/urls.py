
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register.as_view(), name="register"),
    path('checkusername/', views.checkusername, name="checkusername"),
    path('checkemail/', views.checkemail, name="checkemail"),
    path('account/', views.AccountCenter, name="account-center"),
    path('create-profile/', views.CreateProfile.as_view(), name="create-profile"),
    path('profile/', views.profile, name='profile'),
    path('accountvisibility', views.accountvisibility, name="account-visibility"),
    path('updatedsettings', views.updatedsettings, name="updatedsettings"),
    path('changeprofilepicture', views.ChangeProfilePicture.as_view(), name="changeprofilepicture"),
    path('changepassword/', views.PasswordChangeView.as_view(), name="changepassword"),
    path('resetpassword/', views.PasswordResetView.as_view(), name="resetpassword"),
    path('accounts/reset_password_sent', views.PasswordResetDoneView.as_view(), name="password-reset-done"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('newselfie/', views.UploadSelfie.as_view(), name="upload-selfie"),
    path('see-your-selfies/', views.SeeSelfies.as_view(), name="see-your-selfies"),
    path('deletephoto/', views.deletephoto, name="deletephoto"),
    path('find-friends', views.find_friends, name="find-friends"),
    path('find-friends-results', views.find_friend_results, name="find-friends-results"),
    path('add-friend/', views.addfriend.as_view(), name="add-friend"),
    path('friend-requests/', views.friendrequests, name="friend-requests"),
    path('acceptrequest/', views.acceptrequest, name="acceptrequest"),
    path('rejectrequest/', views.rejectrequest, name="rejectrequest"),
    path('myfriends/', views.myfriends, name="myfriends"),
    path('friendprofile', views.friendprofile, name="friendprofile"),
    path('unfriendconfirmation', views.unfriendconfirmation, name="unfriendconfirmation"),
    path('unfriend', views.unfriend, name="unfriend"),
    path('notifications', views.notifications, name="notifications"),
    path('mark-read', views.mark_read, name="mark-read"),
    path('mark-selfie-read', views.mark_photo_read, name="mark-selfie-read"),
    path('mark-all-read', views.mark_all_read, name="mark-all-read"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
