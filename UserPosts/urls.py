from django.urls import path
from .views import UserPosts, PostActions, PostDetailsCurrentUser

urlpatterns = [
    path('Posts/', UserPosts.as_view()),
    path('PostActions/<int:pk>/', PostActions.as_view(), name="GetUpdatePatch"),
    path('CurrentUserPost/', PostDetailsCurrentUser.as_view(), name="GetUpdatePatch"),
]