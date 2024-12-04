
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', include('userprofiles.urls')),
    path('', include('home_and_about_pages.urls')),
]
