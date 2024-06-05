from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return settings.LOGIN_REDIRECT_URL


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    def save_user(self, request, sociallogin, form=None):
        print(sociallogin.user.email)
        user = sociallogin.user
        user.save()
        sociallogin.save(request)
        return user
