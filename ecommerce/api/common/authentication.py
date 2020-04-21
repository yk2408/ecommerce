from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.users.models import Blacklist


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION'][4:]
            try:
                Blacklist.objects.get(token=token)                
                raise AuthenticationFailed('Authentication failed, please re-login.')
            except Blacklist.DoesNotExist:
                pass