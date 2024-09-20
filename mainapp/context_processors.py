from .models import UploadAvatar

def avatar_processor(request):
    if request.user.is_authenticated:        
        avatar_exists = UploadAvatar.objects.filter(user=request.user).exists()
    else:
        avatar_exists = False
    return {
        'avatar_exists' : avatar_exists
    }

def avatar_display_processor(request):
    avatar = None  # Initialize avatar to None
    if request.user.is_authenticated:
        try:
            avatar = UploadAvatar.objects.get(user=request.user)
        except UploadAvatar.DoesNotExist:
            avatar = None    
    return {
        'avatar': avatar
    }