
from captchabreaker.provider import Provider


__all__ = ['_2Captcha']

class _2Captcha(Provider):

    NAME = '2Captcha'

    ENDPOINTS = {'solve':'http://2captcha.com/in.php',
                 'status':'http://2captcha.com/res.php',
                 'report':'http://2captcha.com/res.php',
                 'balance':'http://2captcha.com/res.php'}

    DEFAULT_SETTINGS = {'required_key':False,
                        'report_captchas':False,
                        'captcha_variable_name':'key'}


