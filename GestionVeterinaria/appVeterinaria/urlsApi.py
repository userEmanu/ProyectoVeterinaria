from django.urls import path
from . import apiView

urlpatterns = [
     path('UserList',apiView.userList.as_view())
]