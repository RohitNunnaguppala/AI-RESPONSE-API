# exceptions.py
from rest_framework.exceptions import APIException
from rest_framework import status

class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'
    default_code = 'bad_request'

    def __init__(self, detail=None, code=None):
        self.detail = detail if detail else self.default_detail
        self.code = code if code else self.default_code
