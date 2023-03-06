from rest_framework.views import Response
from rest_framework import status


class ApiResponse:
    @staticmethod
    def sucess(message):
        return Response(
            data=message,
            status=status.HTTP_201_CREATED,
            content_type="application/json")

    @staticmethod
    def failure(error_message):
        return Response(
            data=error_message,
            status=400,
            content_type="application/json")
