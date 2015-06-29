#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
# from setuptools.command.test import test as TestCommand
import os
import re
import sys


# Borrowed from the infamous
# https://github.com/tomchristie/django-rest-framework/blob/master/setup.py
def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


# Borrowed from the infamous
# https://github.com/tomchristie/django-rest-framework/blob/master/setup.py
def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


# Borrowed from the infamous
# https://github.com/tomchristie/django-rest-framework/blob/master/setup.py
def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('okapi')


if sys.argv[-1] == 'publish-test':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push origin master")
    os.system("git push --tags")
    os.system("python setup.py sdist upload -r pypitest")
    sys.exit()


CLASSIFIERS = [
    "Framework :: Kivy",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
]

INSTALL_REQUIRES = [
]

setup(
    name="okapi",
    packages=get_packages("okapi"),
    package_data=get_package_data("okapi"),
    version=version,
    description="Grid-based game framework built on top of Kivy 1.9",
    url="https://github.com/craiglabenz/okapi",
    download_url="https://github.com/craiglabenz/okapi/tarball/{0}".format(version),
    keywords=["kivy", "games", "grid", "grid-based"],
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    author="Craig Labenz",
    author_email="craig.labenz@gmail.com",
    license="MIT"
)
