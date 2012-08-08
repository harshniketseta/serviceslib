#!/usr/bin/env python
from setuptools import find_packages, setup
from glob import glob

import serviceslib

setup(name='serviceslib',
      version=serviceslib.__version__,
      description='A Python library to make calls to Drupal Services painless.',
      long_description=serviceslib.__doc__,
      author=serviceslib.__author__,
      author_email='harshniketseta@gmail.com',
      url='',
      packages=find_packages(),
      data_files=[ ('docs', glob('docs/source/*.rst') + ['docs/source/conf.py' ]) ],
      license='GPLv2',
      platforms = 'any',
     )
