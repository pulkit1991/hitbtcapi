# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

class HitBTCError(Exception):
    """
    Base error class for all exceptions raised in this library.
    Will never be raised naked; more specific subclasses of this exception will be raised when appropriate.
    """

class ParameterRequiredError(HitBTCError): pass

# response error handling
class APIError(HitBTCError):
    """
    Raised for errors related to interaction with the HitBTC API server.
    """
    def __init__(self,status_code,error_msg,error_desc):
        self.status_code = status_code
        self.error_msg = error_msg or ''
        self.error_desc = error_desc or ''
        if self.error_desc:
            self.error_desc = '(%s)' % self.error_desc

    def __str__(self):
        return '%s %s %s' % (self.status_code,self.error_msg,self.error_desc)



class InvalidRequestError(APIError): pass
class AuthenticationError(APIError): pass
class TwoFactorRequiredError(APIError): pass
class InvalidScopeError(APIError): pass
class NotFoundError(APIError): pass
class ValidationError(APIError): pass
class RateLimitExceededError(APIError): pass
class InternalServerError(APIError): pass
class ServiceUnavailableError(APIError): pass
class GatewayTimeoutError(APIError): pass

def api_response_error(response):
    """
    Helper method for creating errors and attaching HTTP response details to them.
    """
    error_msg = str(response.reason) or ''
    error_desc = ''
    if 'json' in response.headers.get('content-type'):
        error = response.json().get('error',None)
        if error:
            error_msg = error.get('message',None)
            error_desc = error.get('description',None)

    error_class = _status_code_to_class.get(response.status_code,APIError)
    return error_class(response.status_code,error_msg,error_desc)



_status_code_to_class = {
    400: InvalidRequestError,
    401: AuthenticationError,
    402: TwoFactorRequiredError,
    403: InvalidScopeError,
    404: NotFoundError,
    422: ValidationError,
    429: RateLimitExceededError,
    500: InternalServerError,
    503: ServiceUnavailableError,
    504: GatewayTimeoutError,
  }
