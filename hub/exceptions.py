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
                "details": {},
            },
            status=500,
        )

    code = getattr(exc, "default_code", "api_error")

    if isinstance(response.data, dict) and "detail" in response.data:
        message = str(response.data["detail"])
        details = {}
    else:
        message = "Validation failed."
        details = response.data if isinstance(response.data, dict) else {}

    response.data = {
        "code": code,
        "message": message,
        "details": details,
    }
    return response