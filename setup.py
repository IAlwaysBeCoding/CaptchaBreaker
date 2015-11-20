#!/usr/bin/python

from setuptools import setup, find_packages

version = '0.0.1'
packages = ['captchabreaker']
setup(name='captchabreaker',
      version=version,
      description="Captcha breaker api framework",
      long_description="",
      # Strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
      'Intended Audience :: Developers',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='MIT',
      packages = find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite='nose.collector'
      )
