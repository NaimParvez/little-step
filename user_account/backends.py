from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to get the user by username first
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            # If no user is found by username, try by email
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                return None

        # If user exists, check password
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except ObjectDoesNotExist:
            return None