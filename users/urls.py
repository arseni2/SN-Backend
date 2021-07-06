from django.urls import path, include

from users.views import UserList

urlpatterns = [
    path('test/', UserList.as_view())
]