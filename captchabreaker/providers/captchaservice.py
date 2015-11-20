
import requests
import path
import urlobject
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from captchabreaker.provider  import Provider
from captchabreaker.exception import (Timeout,MissingKey,InvalidSettings,InvalidCaptcha)
from captchabreaker.version   import VERSION


__all__ = ['CaptchaService']


class CaptchaService(Provider):

    NAME = 'CaptchaService'

    USER_AGENT = 'CaptchaBreaker v{version}'.format(version=VERSION)

    ENDPOINTS = {'solve':None,
                 'status':None,
                 'report':None,
                 'balance':None}

    DEFAULT_SETTINGS = {'required_key':False,
                        'report_captchas':False,
                        'captcha_variable_name':'captchafile'}

    def __init__(self,key=None,settings={}):

        self.verify_endpoints()
        self._key = key

        config = dict(self.DEFAULT_SETTINGS)
        config.update(settings)

        for attr_name in config:
            setattr(self,attr_name,config[attr_name])

        if self.requires_key():
            if not self.has_key():
                raise MissingKey('Missing key for provider:' \
                                 '{provider_name}'.format(provider_name=self.NAME)
                                 )

    def check_balance(self,settings={}):
        """ Checks balance on the captcha provider and returns
            a float specifying how much money there is left
            on the account
        """

    def solve(self,captcha_image,poll=True,sleep=3,retries=10,settings={}):
        """Sends an image to the captcha provider for solving.
            Polling is also avainable which will keep polling
            the captcha provider for a status until the maximum
            number of retries.If the captcha hasn't been solved
            when the maximum amount of tries has been reached,
            then a Timeout exception will be raised.You can specify
            the maximum number of times to poll and the time between
            each poll in seconds.

            With polling set to false, then a 2 item tuple will
            be returned.
                * The first item in the tuple will be a boolean
                  with the value False if the captcha was not solved
                  else it will return the answer to the captcha.

                * The second item is either None or a captcha id
                  that can be used for polling the status of the submitted
                  captcha image.
        """

        try:

            with open(captcha_image,'rb') as f:

                headers = {'User-Agent':self.USER_AGENT}
                post = []
                url = self.ENDPOINT['solve']

                url,post,headers = self.process_settings(url=url,
                                                         post_data=post,
                                                         headers=headers,
                                                         settings=settings)
                if self.requires_key():
                    self.add_key(data=post)

                captcha_handle = f.read()
                captcha_file_name = path.Path(captcha_image).name
                captcha = (self.captcha_variable_name,(captcha_file_name,captcha_handle))

                post.append(captcha)

                encoder = MultipartEncoder(post)
                monitor = MultipartEncoderMonitor(encoder)

                headers.update({'Content-Type':monitor.content_type})

                provider_response = requests.post(url,data=monitor,headers=headers)

                parse = self.parse_response(response=provider_response,settings=settings)


        except IOError:
            raise InvalidCaptcha('Cannot open captcha image:{img}'.format(img=captcha_image))

        else:
            return parse

    def check_status(self,captcha_id,settings={}):
        pass

    def report(self,captcha_id,settings={}):
        pass

    def poll(self,captcha_id,times=10,sleep=3,settings={}):


        try:
            for retry_num in xrange(0,times,1):

                self.check_status(captcha_id=captcha_id,
                                  settings=settings)


            else:
                raise TimeOut('Failed polling captcha service :{service} ' \
                              'Polled {times} times with a sleep of {sleep} ' \
                              'seconds between each status check and did not ' \
                              'received a solved captcha.'.format(service=self.NAME,
                                                                  times=times,
                                                                  sleep=sleep)
                              )
        except:
            pass
        else:



    def parse_response(self,response,settings={}):
        """ parses captcha response and either raises an
            exception or returns text
        """
        raise NotImplementedError('parse_response needs to be ' \
                                  'implemented for provider:' \
                                  '{provider}'.format(provider=self.NAME)
                                  )

    def process_settings(self,url,post_data,headers,settings={}):

        extra = {}
        extra['query']   = settings.get('query',{})
        extra['data']    = settings.get('data',{})
        extra['headers'] = settings.get('headers',{})

        for setting in extra:
            if not isinstance(extra[setting],dict):
                raise InvalidSettings('Invalid setting:{setting} ,it ' \
                                      'needs to be a dictionary of ' \
                                      'additional settings.Instead, '\
                                      'it got an instance of:{instance}'.format(setting=setting,
                                                                                instance=extra[setting])
                                      )

        url = urlobject.URLObject(url)
        url = str(url.query.add_params(extra['query']))

        if isinstance(post_data,dict):
            post_data.update(extra['data'])

        if isinstance(post_data,list):

            for item in extra['data']:
                post_data.append((item,extra['data'][item]))

        headers.update(extra['headers'])

        return (url,post_data,headers)
