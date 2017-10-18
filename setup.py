#!/usr/bin/env python

import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  python setup.py tag")
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a v%s -m 'Version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup()
