from django.contrib.auth.models import User
from django.conf.urls.static import static
from account.models import Profile

def create_profile(backend, user, *args, **kwargs):
    """
        Create user profile for social authentication
    """
    Profile.objects.get_or_create(user=user, photo='default_profile.png')
    # add @ to username
    user.username = '@' + user.username if not user.username.startswith('@') else user.username

