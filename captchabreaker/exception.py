

__all__ = ['CaptchaBreakerException','CBProviderException','MissingKey',
           'InvalidKey','Timeout','InvalidProvider','InvalidData',
           'InvalidEndpoint''InvalidSettings','InvalidCaptcha',
           'CBSolverException','UnsolvedCaptcha']


class CaptchaBreakerException(Exception):
    pass

class CBProviderException(CaptchaBreakerException):
    pass

class MissingKey(CBProviderException):
    pass

class InvalidKey(CBProviderException):
    pass

class Timeout(CBProviderException):
    pass

class InvalidProvider(CBProviderException):
    pass

class InvalidData(CBProviderException):
    pass

class InvalidEndpoint(CBProviderException):
    pass

class InvalidSettings(CBProviderException):
    pass

class InvalidCaptcha(CBProviderException):
    pass

class CBSolverException(CaptchaBreakerException):
    pass

class UnsolvedCaptcha(CBSolverException):
    pass
