from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    print(22222)
    if response is None:
        return Response(
            {"error": "这里有一个错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)
    return response
