from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from userprofile.models import User
from api.common.utils import get_error_message
from django.core.exceptions import ValidationError
from rest_framework import exceptions as rest_exceptions


def get_response(message="", result={}, status=True, status_code=200):
    return {
        "message" : message,
        "result" : result,
        "status" : status,
        "status_code" : status_code,
    }


class BaseView(APIView):
    # will be use for put the common code like, pagination, sorting etc ..
    expected_exceptions = {
        ValidationError: rest_exceptions.ValidationError
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
    pass

    
