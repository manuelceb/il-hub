from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "code": "internal_error",
                "message": "An unexpected error occurred.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    code = getattr(exc, "default_code", "api_error")

    if isinstance(response.data, dict) and "detail" in response.data:
        message = str(response.data["detail"])
    else:
        message = "Validation failed."

    response.data = {
        "code": code,
        "message": message,
    }
    return response
