from rest_framework.mixins import CreateModelMixin, ListModelMixin
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
import json
from rest_framework.pagination import LimitOffsetPagination

class CreateUserView(CreateModelMixin, GenericAPIView):
    """
    Create user
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ListUsersView(ListModelMixin, GenericAPIView):
    """
    List user view
    """
    queryset = User.objects.all()
    serializer_class = ListUsers
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def filter_queryset(self,queryset):
        if self.request.GET.get("query"):
            queryset = queryset.filter(Q(first_name__icontains=self.request.GET.get("query")) | Q(email__icontains=self.request.GET.get("query")))

        return queryset
    
class ManageFriendRequest(APIView):
    """This API is used for sending, accepting or rejecting friend request"""
    def post(self, request):
        try:
            data = request.body.decode("utf-8")
            if data:
                serializer = FriendRequest(data=json.loads(data), request=request)
                if serializer.is_valid():
                    message = serializer.save()
                    return Response({"message":message}, status=200)
                
                return Response(serializer.errors, status=400)
            else:
                return Response({"error":"please provide request body"}, status=400)

        except Exception as e:
            return Response({"error":f"Exception occured, message: {e}"}, status=500)


class PendingFriendRequest(APIView, LimitOffsetPagination):
    """
    List all pending friend requests.
    """
    serializer_class = ListUsers

    def get(self, request, format=None):
        usr_obj, created = UserProfile.objects.get_or_create(user=request.user)
        f_requests = usr_obj.frend_requests.all()
        results = self.paginate_queryset(f_requests, request)
        serializer = self.serializer_class(results, many=True)
        return self.get_paginated_response(serializer.data)

class ListFriends(APIView, LimitOffsetPagination):
    """
    List all pending friend requests.
    """
    serializer_class = ListUsers

    def get(self, request, format=None):
        usr_obj, created = UserProfile.objects.get_or_create(user=request.user)
        f_requests = usr_obj.friends.all()
        results = self.paginate_queryset(f_requests, request)
        serializer = self.serializer_class(results, many=True)
        return self.get_paginated_response(serializer.data)