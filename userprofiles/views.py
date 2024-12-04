from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Selfies, Profile, FriendJunctionTable, FriendRequestJunctionTable, FriendRequests, Friends, Notification, NotifierJunctionTable
from .forms import SignUpForm, UploadSelfieForm, CreateProfileForm
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.views.generic import FormView
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.db.models.functions import Concat
from django.db.models import CharField, Value


#///////////////////////////////// SIGNIN / SIGNOUT /////////////////////////////////

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error."))
            return redirect('register')
    else:
        return render(request, 'signin.html', {})

def signout(request):
    logout(request)
    messages.success(request, ("You are now signed out"))
    return redirect('home')



#///////////////////////////////// REGISTER /////////////////////////////////

class register(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('signin')
    template_name = 'register.html'

# Username already exists or is available

def checkusername(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username):
        return HttpResponse("<div style='color: red;'>This username already exists</div>")
    else:
        return HttpResponse("<div style='color: green;'>This username is available</div>")


def AccountCenter(request):
    return render(request, 'accountcenter.html')


class CreateProfile(CreateView):
    form_class = CreateProfileForm
    template_name = 'createprofile.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args):
        if self.request.user.is_authenticated is False:
            return redirect('home')
        else:
            profile = {}
            profile['form'] = CreateProfileForm()
            return render(request, "createprofile.html", profile)
            # try:
            #     profile = Profile.objects.get(user=request.user)
            #     dict = {'profile': profile}
            #     return render(request, 'createprofile.html', {'profile': dict})
            # except:
            #     profile = {}
            #     profile['form'] = CreateProfileForm()
            #     return render(request, "createprofile.html", profile)
    
    def post(self, request, *args):
        context = {}
        context['form'] = CreateProfileForm()
        if request.method == "POST":
            currentuser = request.user
            user = User.objects.get(id=currentuser.id)
            # currentuser = Profile(user=user)
            try:
                j = Profile.objects.get(user=user)
            except:
                j, created = Profile.objects.get_or_create(user=user, first_name="", last_name="", birthday="2024-01-01", profilepicture="images/unknown-user.png")
            # k = Profile(user=user)
            f = CreateProfileForm(request.POST, request.FILES, instance=j)
            if f.is_valid():
                f.save(commit=False)
                f.user = request.user
                f.save()
                messages.success(request, 'Your profile is now updated')
            else:
                messages.error(request, 'Uh-oh. Something went wrong... Maybe you can try again.')

        return render(request, "createprofile.html", context)



#///////////////////////////////// PROFILE /////////////////////////////////

def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'profile.html', {"profile": profile})
    except:
        return redirect('create-profile')

def accountvisibility(request):
    user=request.user
    currentsettings = Profile.objects.filter(user=user)
    return render(request, 'accountvisibility.html', {"currentsettings": currentsettings})

def updatedsettings(request, *args, **kwargs):    
    a = request.POST["accountvisibility"]
    user = request.user
    try:
        currentsettings = Profile.objects.get(user=user)
        if a == "false":
            currentsettings.publicaccount = False
            currentsettings.save()
            return render(request, 'accountcenter.html', {"currentsettings": currentsettings})
        else:
            currentsettings.publicaccount = True
            currentsettings.save()
            return render(request, 'accountcenter.html', {"currentsettings": currentsettings})
    except:
        currentsettings = Profile.objects.create(user=user, publicaccount=False)
        if a == "false":
            currentsettings.publicaccount = False
            currentsettings.save()
            return render(request, 'accountcenter.html', {"currentsettings": currentsettings})
        elif a == "true":
            currentsettings.publicaccount = True
            currentsettings.save()
            return render(request, 'accountcenter.html', {"currentsettings": currentsettings})

class ChangeProfilePicture(CreateView):
    template_name = 'changeprofilepicture.html'
    success_url = reverse_lazy('changeprofilepicture')

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            return render(request, 'changeprofilepicture.html', {'profile': profile})
        except:
            return redirect(request, 'index.html')
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            profile = Profile.objects.get(user=request.user)
            data = request.FILES.get('picture')
            profile.profilepicture = data
            profile.save()
            messages.success(request, "Your profile picture has been updated. Rock on.")
            return render(request, 'changeprofilepicture.html', {})



#///////////////////////////////// SELFIES /////////////////////////////////

class UploadSelfie(CreateView):
    form_class = UploadSelfieForm
    template_name = 'upload-new-selfie-page.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args):
        if self.request.user.is_authenticated is False:
            return redirect('home')
        else:
            context = {}
            context['form'] = UploadSelfieForm()
            if request.method == 'POST':
                currentuser = request.user
                user = User.objects.get(id=currentuser.id)
                currentuser = Selfies(user=user)
                f = UploadSelfieForm(request.POST, request.FILES, instance=currentuser)
                if f.is_valid():
                    f.save(commit=False)
                    f.user = request.user
                    f.save()
                    messages.success(request, 'Awesome! You have updated your gallery!')
                else:
                    messages.error(request, 'Uh-oh. Something went wrong... Maybe you can try again.')

            return render(request, "upload-new-selfie-page.html", context)

    def post(self, request, *args):
        context = {}
        context['form'] = UploadSelfieForm()
        if request.method == 'POST':
            currentuser = request.user
            user = User.objects.get(id=currentuser.id)
            currentuser = Selfies(user=user)
            f = UploadSelfieForm(request.POST, request.FILES, instance=currentuser)
            if f.is_valid():
                f.save(commit=False)
                f.user = request.user
                f.save()
                messages.success(request, 'Awesome! You have updated your gallery!')
            else:
                messages.error(request, 'Uh-oh. Something went wrong... Maybe you can try again.')

        # return render(request, "upload-new-selfie-page.html", context)
        return redirect('see-your-selfies')


class SeeSelfies(TemplateView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            selfies = Selfies.objects.filter(user=request.user)
            dict = {'selfies': selfies}
            return render(request, 'see-your-selfies.html', {'selfies': dict})
        else:
            return redirect('home')

def deletephoto(request, *args):
    photo=request.POST.get('deletebutton')
    selfietobedeleted = Selfies.objects.get(id=photo)
    selfietobedeleted.delete()
    return redirect('see-your-selfies')


# def checkusername(request):
#     username = request.POST.get('username')
#     if get_user_model().objects.filter(username=username):
#         return HttpResponse("<div style='color: red;'>This username already exists</div>")
#     else:
#         return HttpResponse("<div style='color: green;'>This username is available</div>")

# class signin(request):
#     success_url = lazy


#///////////////////////////////// FRIENDS /////////////////////////////////

def find_friends(request, *args):
    name = request.POST.get('searchedforname')
    results = Profile.objects.filter(first_name=name)
    return render(request, 'findfriends.html', {"results": results})

def find_friend_results(request, *args, **kwargs):
    name = request.POST.get('searchedforname')
    j = Profile.objects.annotate(fullname=Concat('first_name',  Value(' '), 'last_name', output_field=CharField()))
    results = j.filter(publicaccount=True)
    res = results.filter(fullname__icontains=name)
    return render(request, 'findfriends.html', {"res": res})


def addfriend(request):
    person = request.POST.get('newfriend')
    joker = User.objects.get(id=person)
    friend = request.POST.get('friend')
    # the junction table is empty
    # so the queryset is empty
    # friendtoadd = User.objects.filter(id=person)
    requester = FriendRequestJunctionTable.objects.get_or_create(user=request.user)
    # l = FriendRequestJunctionTable.objects.all()
    k = FriendRequestJunctionTable.objects.get(user=request.user)
    friendrequest = FriendRequests.objects.get_or_create(user=joker, requester=k)
    l = FriendRequests.objects.all()
    messages.success(request, "Your request has been sent")
    return render(request, 'addfriend.html', {'l': l})

class addfriend(TemplateView):
    permission_classes = [IsAuthenticated]
    template_name = "addfriends.html"

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            person = request.POST.get('newfriend')
            joker = User.objects.get(id=person)
            friend = request.POST.get('friend')
            # the junction table is empty
            # so the queryset is empty
            # friendtoadd = User.objects.filter(id=person)
            requester = FriendRequestJunctionTable.objects.get_or_create(user=request.user)
            # l = FriendRequestJunctionTable.objects.all()
            k = FriendRequestJunctionTable.objects.get(user=request.user)
            friendrequest = FriendRequests.objects.get_or_create(user=joker, requester=k)
            l = FriendRequests.objects.all()
            messages.success(request, "Your request has been sent")
            notifier_j_t = NotifierJunctionTable.objects.create(user=request.user)
            Notification.objects.create(user=joker, message="You have a new friend request from", notifier=notifier_j_t)
            return render(request, 'addfriend.html', {'l': l})
        else:
            messages.error(request, "You must be signed in to make a friend request")
            return render(request, "signin.html")

def friendrequests(request):
    current_requests = FriendRequests.objects.filter(user=request.user)
    return render(request, 'friendrequests.html', {'current_requests': current_requests})

def acceptrequest(request):
    response = request.POST.get('requestbutton')
    # friend = request.GET.get('friend')
    # Friend object for requestee
    gettingfriend = User.objects.get(id=response)
    creatingnewobject = FriendJunctionTable.objects.get_or_create(user=gettingfriend)
    requester = FriendJunctionTable.objects.get(user=gettingfriend)
    friend_and_status = Friends.objects.get_or_create(user=request.user, friend=requester, friendstatus=True)
    # Friend object for requester
    currentuser = User.objects.get(id=request.user.id)
    objectforcurrentuser = FriendJunctionTable.objects.get_or_create(user=currentuser)
    requestee = FriendJunctionTable.objects.get(user=currentuser)
    friend_and_status2 = Friends.objects.get_or_create(user=gettingfriend, friend=requestee, friendstatus=True)
    # Deleting request
    requester_friendrequestjunctiontable = FriendRequestJunctionTable.objects.get(user=gettingfriend)
    currentrequest = FriendRequests.objects.filter(user=request.user, requester=requester_friendrequestjunctiontable)
    currentrequest.delete()
    # return render(request, 'friendrequests.html', {'friend_and_status': friend_and_status})
    return redirect('friend-requests')
    
def rejectrequest(request):
    response = request.POST.get('requestbutton')
    # friend = request.GET.get('friend')
    # Friend object for requestee
    gettingfriend = User.objects.get(id=response)
    creatingnewobject = FriendJunctionTable.objects.get_or_create(user=gettingfriend)
    requester = FriendJunctionTable.objects.get(user=gettingfriend)
    friend_and_status = Friends.objects.get_or_create(user=request.user, friend=requester, friendstatus=False)
    # Friend object for requester
    currentuser = User.objects.get(id=request.user.id)
    objectforcurrentuser = FriendJunctionTable.objects.get_or_create(user=currentuser)
    requestee = FriendJunctionTable.objects.get(user=currentuser)
    friend_and_status2 = Friends.objects.get_or_create(user=gettingfriend, friend=requestee, friendstatus=False)
    # Deleting request
    requester_friendrequestjunctiontable = FriendRequestJunctionTable.objects.get(user=gettingfriend)
    currentrequest = FriendRequests.objects.filter(user=request.user, requester=requester_friendrequestjunctiontable)
    currentrequest.delete()
    return render(request, 'friendrequests.html', {'friend_and_status': friend_and_status})

def myfriends(request):
    friends = Friends.objects.filter(user=request.user)
    myfriends = friends.filter(friendstatus=True)
    # for item in myfriends:
    people = Profile.objects.all()
    # profiles = Profile.objects.all()
    return render(request, 'myfriends.html', {'myfriends': myfriends, 'people': people})

def unfriendconfirmation(request):
    # friends = Friends.objects.filter(user=a)
    # myfriends = friends.filter(friendstatus=True)
    junctiontablenumber = request.POST.get('unfriendconfirmationbutton')
    l = FriendJunctionTable.objects.get(id=junctiontablenumber)
    # l = r.user
    # l = User.objects.get(username=p)
    return render(request, 'unfriendconfirmation.html', {"l": l})

def unfriend(request):
    a = request.user.id
    # friends = Friends.objects.filter(user=a)
    # myfriends = friends.filter(friendstatus=True)
    junctiontablenumber = request.POST.get('unfriendbutton')
    r = FriendJunctionTable.objects.get(id=junctiontablenumber)
    p = r.user
    # mate = User.objects.get(id=fr)
    # persontobeunfriended = friends.filter(friend=fr)
    fjt = FriendJunctionTable.objects.filter(user=request.user)
    j = Friends.objects.get(user=a, friend=junctiontablenumber, friendstatus=True)
    for items in fjt:
        try:
            k = Friends.objects.get(user=p, friend=items, friendstatus=True)
            z = FriendJunctionTable.objects.get(id=items.id)
            k.delete()
            z.delete()
        except:
            pass
    # persontobeunfriended.delete()
    j.delete()

    r.delete()
    # k = mate.id

    friends2 = Friends.objects.filter(friend=a)
    # # # myfriends = friends.filter(friendstatus=True)
    # # # friend = request.POST.get('unfriendbutton')
    # request.user.id
    # request.user.id
    # for i in friends2:
    #     if i.friend == request.user:
    #         i.delete()
    # persontobeunfriended2 = friends2.filter(friend=a)
    # persontobeunfriended2.delete()

    return render(request, 'unfriend.html')

def friendprofile(request):
    friend_id = request.POST.get('friendprofilebutton')
    friends_profile = Profile.objects.get(id=friend_id)
    selfies = Selfies.objects.filter(user=friend_id)
    dict = {'selfies': selfies}
    return render(request, 'friendprofile.html', {'friends_profile': friends_profile, 'selfies': dict})



#///////////////////////////////// NOTIFICATIONS /////////////////////////////////

def notifications(request):
    notifica = Notification.objects.filter(user=request.user)
    notifications = notifica.filter(is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})

def mark_unread(request):
    update = request.POST.get('update')
    noti = Notification.objects.get(id=update)
    noti.is_read = True
    noti.save()
    return redirect('notifications')