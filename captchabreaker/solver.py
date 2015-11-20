
import os
import abc
from functools import partial

import six

from captchabreaker.provider   import Provider
from captchabreaker.exception  import (CaptchaBreakerException,InvalidProvider,
                                       Timeout,UnsolvedCaptcha)


__all__ = ['Solver']

@six.add_metaclass(abc.ABCMeta)
class Solver(object):

    DEFAULT_SETTINGS = {'poll':True,
                        'poll_sleep':3,
                        'poll_max':10,
                        'retry':True,
                        'retry_max':3,
                        'save':False,
                        'save_folder':os.getcwd()}

    def __init__(self,providers,settings={}):

        self._providers = providers

        config = dict(self.DEFAULT_SETTINGS)
        config.update(settings)

        for attr_name in config:
            setattr(self,attr_name,config[attr_name])

    def __call__(self,captcha_file,provider=None,include_id=False):

        def maximum_tries_reached(tries,max):

            return tries == max

        tries = int(self.retry_max) if self.retry else 1
        next_provider = partial(self.get_next_provider,
                                captcha_file=captcha_file,
                                provider=provider,
                                max_tries=tries-1)

        retry = partial(maximum_tries_reached,max=tries-1)

        for attempt_num in xrange(0,tries,1):

            provider = next_provider(current_try=attempt_num)
            try:
                response,captcha_id = self.solve_captcha(captcha_file=captcha_file,
                                                         provider_name=provider)


            except Timeout:
                if retry(tries=attempt_num):continue

                raise Timeout('Reached maximum allowed polling '\
                            'retries:{retries}. Captcha has '\
                            'been unsolved'.format(retries=self.retry_max)
                            )

            except CaptchaBreakerException as ex:
                if retry(tries=attempt_num):continue

                raise ex(ex.message)

            else:
                if response is None:continue

                return (response,captcha_id) if include_id else response

        else:
            raise UnsolvedCaptcha('Captcha was unsolved, and no '\
                                'additional polling was done')

    @abc.abstractmethod
    def get_next_provider(self,captcha_file,provider_name,current_try,max_tries):
        pass

    def __getitem__(self,k):
        try:
            return self._providers[k]
        except KeyError:
            raise InvalidProvider('The provider name:{k} does not exist'.format(k=k))

    @abc.abstractmethod
    def get_provider(self,name):
        pass

    @abc.abstractmethod
    def get_solved_filename(self,provider_name,captcha_id,solved_text,captcha_file):
        pass

    @staticmethod
    def verify_providers(providers):

        if not isinstance(providers,dict):
            raise InvalidProvider('providers is not a valid '\
                                  'dictionary containing keys '\
                                  'with Providers instances as '\
                                  'values')

        check_iter = iter([(key,providers[key]) for key in providers])

        while True:
            try:
                name,provider = next(check_iter)

                if not isinstance(provider,Provider):
                    raise InvalidProvider('Got an invalid provider '\
                                          'instance :{provider} for '\
                                          'key:{key}'.format(provider=provider,
                                                             key=name)
                                          )


            except StopIteration:
                break

    @abc.abstractmethod
    def providers(self):
        pass

    @abc.abstractmethod
    def solve_captcha(self,captcha_file,provider_name):
        pass

