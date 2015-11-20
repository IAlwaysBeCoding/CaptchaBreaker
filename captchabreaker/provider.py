
import abc

import six

from captchabreaker.exception import (InvalidKey,MissingKey,InvalidData,
                                      InvalidEndpoint)


__all__ = ['Provider']


@six.add_metaclass(abc.ABCMeta)
class Provider(object):


    DEFAULT_SETTINGS = {'required_key':False,
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

    @abc.abstractmethod
    def check_balance(self,settings={}):
        """ Checks balance on the captcha provider and returns
            a float specifying how much money there is left
            on the account
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def check_status(self,captcha_id,settings={}):
        """ Checks status of the captcha submitted. This
            method is used for polling in a loop"""

    @abc.abstractmethod
    def report(self,captcha_id,settings={}):
        """ Reports a captcha as an incorrect captcha
            text received as an answer
        """

    def poll(self,captcha_id,times=10,sleep=3,settings={}):
        """ Loops on checking status of the captcha submitted.
            It will sleep between each  call and if the captcha
            hasn't been solved after polling a maximum amount
            of times, then it will raise a Timeout exception
        """

    def add_key(self,data):

        key = self.get_key()

        if isinstance(data,dict):
            data.update(key)
            return data

        if isinstance(data,list):
            for name in key:
                data.append((name,key[name]))

            return data

        raise InvalidData('Cannot sign key with data '\
                          'make sure data is a list or a '\
                          'dictionary containing the post '\
                          'data that will be used to submit '\
                          'to the provider in a POST')

    def requires_key(self):
        return self.required_key
    def has_key(self):
        return True if self._key else False

    def get_key(self):

        if not self.has_key():
            raise MissingKey('Missing key')

        if not isinstance(self._key,dict):
            raise InvalidKey('Current key set is not a dictonary '\
                             'instance, please set a dictionary '\
                             'with keys for authentication')

        return self._key

    def set_key(self,value):
        if not isinstance(value,dict):
            raise InvalidKey('Key needs to be an dictionary '\
                             'instance with 1 or more keys '\
                             'to pass to the post data as '\
                             'authentication')

    def delete_key(self):
        self._key = None

    @abc.abstractmethod
    def parse_response(self,response,settings={}):
        """ parses captcha response and either raises an
            exception or returns text
        """

    @abc.abstractmethod
    def process_settings(self,url,post_data,headers,settings={}):
        """
            Adds any extra query parameter, post data, and extra
            headers with the values from the settings dictionary.
        """

    @classmethod
    def verify_endpoints(cls):

        for endpoint in cls.ENDPOINTS:
            if (cls.ENDPOINTS[endpoint] is None) or \
                (type(cls.ENDPOINTS[endpoint]) != str):

                raise InvalidEndpoint('Endpoint:{endpoint} is '\
                                      'an invalid endpoint url '\
                                      'with value:{value}'.format(endpoint=endpoint,
                                                                  value=cls.ENDPOINTS[endpoint])
                                      )


