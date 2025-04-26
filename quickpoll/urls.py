from django.contrib import admin
from django.urls import path, include
from polls.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('polls.urls')),
]