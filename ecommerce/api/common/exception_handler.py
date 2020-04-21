from rest_framework.views import exception_handler
from api.base.views import get_response
from django.http import JsonResponse
import logging
import traceback


def get_error_message(error_dict):
    print("Error-Dict-------------->", error_dict)
    field = next(iter(error_dict))
    print(field)
    response = error_dict[next(iter(error_dict))]
    print(response)
    print(response[0])
    if isinstance(response, dict):
        response = get_error_message(response)
        print('Resonse------------------>', response)
    elif isinstance(response, list):
        response_message = response[0]
        print('Resonse_message------------------>', response_message)
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = response[0]
    return response


def get_first_error_message(error_dict):
    response = error_dict[next(iter(error_dict))]
    print('First_Response--------->', response)
    if isinstance(response, dict):
        response = get_first_error_message(response)
    elif isinstance(response, list):
        response = response[0]
        if isinstance(response, dict):
            response = get_first_error_message(response)
    return response


def custom_exception_handler(exc, context):
    print('Context------------->', context)
    error_response = exception_handler(exc, context)
    print('Data', error_response.data)
    if error_response is not None:
        error = error_response.data
        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = get_response(
                    message=get_error_message(error),
                    status_code=error_response.status_code,
                    status=False
                )

            elif isinstance(error[0], str):
                error_response.data = get_response(
                    message=error[0],
                    status_code=error_response.status_code,
                    status=False
                )

        if isinstance(error, dict):
            error_response.data = get_response(
                message=get_error_message(error),
                status_code=error_response.status_code,
                status=False
            )

    return error_response


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            response = get_response(
                message="Internal server error, please try again later", status=False, status_code=response.status_code)
            return JsonResponse(response, status=response['status_code'])

        if response.status_code == 404 and "<h1>Not Found</h1>" in str(response.content):
            logging.error(response.content)
            response = get_response(status=False, status_code=404, message="Page not found, invalid url")
            return JsonResponse(response, status=response['status_code'])
        return response

    def process_exception(self, request, exception):
        logging.error("ERROR")
        logging.error(traceback.format_exc())
        response = get_response(status=False, status_code=500, message="Internal server error, please try again later")
        return JsonResponse(response, status=response['status_code'])