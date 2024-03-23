from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from .handle_friend_request import *

FRIEND_REQUEST_TYPE = ["send","accept","reject"]

class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=254, required=True)
    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name'),
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ListUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'email']

class FriendRequest(serializers.Serializer):
    r_type = serializers.CharField(max_length=10, required=True)
    user_id = serializers.IntegerField(required=True)

    def __init__(self, instance=None, data=..., **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(instance, data, **kwargs)

    def validate_user_id(self, value):
        if value == self.request.user.id:
            raise serializers.ValidationError(f"User cannot process his own request")
        try:
            self._requested_user = User.objects.get(id=value)
        except:
            raise serializers.ValidationError(f"User id does not exist, please provide correct user id")

        return value

    def validate(self, data):
        response =  super().validate(data)
        r_type = data["r_type"]

        self.requested_userprofile_obj, created = UserProfile.objects.get_or_create(user=self._requested_user)
        self.current_userprofile_obj, created = UserProfile.objects.get_or_create(user=self.request.user)

        if r_type in ["accept","reject"]:
            if self._requested_user not in self.current_userprofile_obj.frend_requests.all():
                raise serializers.ValidationError(f"User {self.current_userprofile_obj.user.username} does not have friend request from {self._requested_user.username}.")
            
        return response
    

    def validate_r_type(self, value):
        if value not in FRIEND_REQUEST_TYPE:
            raise serializers.ValidationError(f"r_type should be one of {FRIEND_REQUEST_TYPE}")
        return value
    
    def save(self):
        
        if self.validated_data["r_type"] == "send":
            handle_send(self.current_userprofile_obj, self.requested_userprofile_obj)
            message = "friend request successfully send"
        elif self.validated_data["r_type"] == "accept":
            handle_accept(self.current_userprofile_obj, self.requested_userprofile_obj)
            message = "friend request accepted successfully"

        elif self.validated_data["r_type"] == "reject":
            handle_reject(self.current_userprofile_obj, self.requested_userprofile_obj)
            message = "friend request reject successfully"
        
        return message