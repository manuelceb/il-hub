from rest_framework.exceptions import APIException
from rest_framework import status


class ClientHandlerNotConfigured(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "The registered client has no profile handler configured."
    default_code = "client_handler_not_configured"


class ClientNotRegistered(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "This application is not registered in IL-Hub for profile access."
    default_code = "client_not_registered"


class ContextualProfileNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "No profile exists for this user."
    default_code = "profile_not_found"


class ClientInactive(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The requesting client is inactive."
    default_code = "client_inactive"


class TokenClientError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "The token is not associated with a client application"
    default_code = "token_no_client"
