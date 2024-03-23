from .models import UserProfile

def handle_send(current_user:UserProfile, request_user:UserProfile):
    request_user.frend_requests.add(current_user.user)
    request_user.save()
    return current_user

def handle_accept(current_user:UserProfile, request_user:UserProfile):
    current_user.friends.add(request_user.user)
    current_user.frend_requests.remove(request_user.user)
    current_user.save()
    return current_user
    
def handle_reject(current_user:UserProfile, request_user:UserProfile):
    current_user.frend_requests.remove(request_user.user)
    current_user.save()
    return current_user
