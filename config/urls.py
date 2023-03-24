from django.contrib import admin
from django.urls import path, include

from questions.views import login, register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('questions/', include("django.contrib.auth.urls")),
    path('login/', login, name="login"),
    path('register/', register, name="registration")
]
