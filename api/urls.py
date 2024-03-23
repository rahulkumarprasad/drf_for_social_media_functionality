from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("create-user", CreateUserView.as_view(), name="create_user"),
    path("list-users", ListUsersView.as_view(), name="list_users"),
    path("send-accept-reject/friend-request", ManageFriendRequest.as_view(), name="friend_requests_functions"),
    path("pending-friend-request", PendingFriendRequest.as_view(), name="pending_friend_request"),
    path("list-friends", ListFriends.as_view(), name="list_friends"),

    #token api
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]