from django.db.models.deletion import ProtectedError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, ProtectedError):
        return Response(
            {"detail": "One cannot eliminate the breed according to which the dogs are prescribed."},
            status=status.HTTP_409_CONFLICT,
        )
    return response