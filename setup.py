#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import re
import sys


def readme():
    with open('readme.md') as f:
        return f.read()


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
    "Topic :: Games/Entertainment",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Development Status :: 3 - Alpha",
    "Natural Language :: English",
]

INSTALL_REQUIRES = [
]

setup(
    name="kivy-okapi",
    packages=get_packages("okapi"),
    package_data=get_package_data("okapi"),
    version=version,
    description="Grid-based game framework built with Kivy 1.9",
    long_description=readme(),
    url="https://github.com/craiglabenz/kivy-okapi",
    download_url="https://github.com/craiglabenz/kivy-okapi/tarball/{0}".format(version),
    keywords=["kivy", "python", "python2", "game", "games", "grid", "grid-based"],
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    author="Craig Labenz",
    author_email="craig.labenz@gmail.com",
    license="MIT",
    include_package_data=True,
    zip_safe=False
)
