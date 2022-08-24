from .api_exception import APIException
from .unauthorized import Unauthorized
from .email_exists import EmailExists
from .invalid_email import InvalidEmail
from .invalid_oob_code import InvalidOOBCode
from .invalid_password import InvalidPassword
from .login_is_not_default import LoginIsNotDefault
from .bad_response import BadResponse

_exceptions = {
    "ERROR_UNAUTHORIZED": Unauthorized,
    "EMAIL_EXISTS": EmailExists,
    "INVALID_EMAIL": InvalidEmail,
    "INVALID_OOB_CODE": InvalidOOBCode,
    "INVALID_PASSWORD": InvalidPassword,
    "E_LOGIN_IS_NOT_DEFAULT": LoginIsNotDefault
}


def find_exception(code: str, message: str, params: list):
    exception_message = message if len(message) > 0 else code
    if code in _exceptions: raise _exceptions[code](code, exception_message, params)
    elif message in _exceptions: raise _exceptions[message](code, exception_message, params)
    else: raise APIException(code, exception_message, params)
