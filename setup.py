#!/usr/bin/env python
# coding=utf-8

from setuptools import setup
from webmpris import __version__, __description__, requires, README


setup(name='webmpris',
      version=__version__,
      description=__description__,
      author='Mikhail Mamrouski',
      author_email='wst.public.mail@gmail.com',
      url="https://github.com/wistful/webmpris",
      license="MIT License",
      packages=['webmpris'],
      long_description=README,
      install_requires=requires,
      platforms=["Unix,"],
      keywords="mpris, dbus, django, rest api",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Django",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      )
