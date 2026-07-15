from .models import LibraryContext, BlogContext
from .serializers import BlogContextSerializer, LibraryContextSerializer

def get_user_profile(user, client):
    profile = None
    if client == 'library':
        profile = LibraryContext.objects.filter(user=user).first()
        profile = LibraryContextSerializer(profile).data
    
    if client == 'blog':
        profile = BlogContext.objects.filter(user=user).first()
        profile =  BlogContextSerializer(profile).data
        
    profile["user_uid"] = str(user.user_uid)
    return profile
