from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """This models is used for storing data related to User Details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    frend_requests = models.ManyToManyField(User, related_name="frend_requests")
    friends = models.ManyToManyField(User, related_name="list_frends")

    def __str__(self):
         return f"{self.user.username}"