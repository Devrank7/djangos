from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.db.models import Q

from main.models import User


class MyBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        user = get_user_model()
        try:
            users = user.objects.get(Q(username=username) | Q(email=username))
            if users.check_password(password):
                return users
            return None
        except (user.DoesNotExist, user.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user = get_user_model()
        try:
            return user.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None


####
