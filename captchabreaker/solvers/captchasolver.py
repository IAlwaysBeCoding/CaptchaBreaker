
import os
from functools import partial

from captchabreaker.solver import Solver
from captchabreaker.utils import ensure_dir


__all__ = ['CaptchaSolver']

class CaptchaSolver(Solver):

    def get_next_provider(self,captcha_file,provider_name,current_try,max_tries):

        def rotate_providers(batch,index):
            if index >= len(batch)-1:
                return (batch[0],0)
            else:
                return (batch[index],index)

        next_provider = partial(rotate_providers,batch=self.providers())

        return next_provider()

    def get_provider(self,name):

        provider = self[name]
        check_provider = {name:provider}

        type(self).verify_providers(providers=check_provider)

        return self[name]

    def get_solved_filename(self,provider_name,captcha_id,solved_text,captcha_file):

        ensure_dir(self.save_folder)

        saving_name = '{provider}-' \
                        '{captcha_id}-' \
                        '{solved_text}-' .format(provider=provider_name,
                                                captcha_id=captcha_id,
                                                solved_text=solved_text)
        loc = (self.save_folder,saving_name)
        return os.path.join(**loc)

    def providers(self):
        return [p for p in self._providers]

    def solve_captcha(self,captcha_file,provider_name):

        provider = self.get_provider(name=provider_name)
        result,captcha_id = provider.solve(captcha_file,
                                            poll=self.poll,
                                            sleep=self.poll_sleep,
                                            retries=self.poll_max)
        if self.save:
            saving_name = self.get_solved_filename(provider_name=provider_name,
                                                   captcha_id=captcha_id,
                                                   solved_text=result,
                                                   captcha_file=captcha_file)




