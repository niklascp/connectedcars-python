#!/usr/bin/env python
from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    install_requires = [line.rstrip('\r\n') for line in file]

setup(
  name = 'connectedcars',
  packages = ['connectedcars'],
  version = '0.1.3',
  license = 'MIT',
  description = 'Wrapper for access the Connected Cars API - an AVL/data collection service installed in most new danish vehicles from Audi, Volkswagen, Skoda and SEAT.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Niklas Christoffer Petersen',
  author_email = 'nikalscp@gmail.com',
  url = 'https://github.com/niklascp/connectedcars-python',
  download_url = 'https://github.com/niklascp/connectedcars-python/archive/v0.1.0.tar.gz',
  keywords = ['AVL', 'Audi', 'Volkswagen', 'Skoda', 'SEAT'],
  install_requires = install_requires,
  classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
