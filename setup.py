#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for the `mult-mixins` Django project."""

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

# Standard library
import io
import logging
import os
import sys
from shutil import rmtree

# Third-party
from setuptools import Command, find_packages, setup

logger = logging.getLogger(__name__)

# Package meta-data.
NAME = 'dj-mult-mixins'
DESCRIPTION = 'Django app to help a team to know who has to buy the breakfast.'
URL = 'https://github.com/hbuyse/dj-mult-mixins'
EMAIL = 'henri.buyse@gmail.com'
AUTHOR = 'Henri Buyse'
REQUIRES_PYTHON = '>=3.4.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "Django>=2.0,<2.2",
    "django-markdownx>=2.0.28",
]

# What packages are optional?
EXTRAS = {
    'dev': [
        'flake8',
        'flake8-docstrings>=0.2.7',
        'flake8-rst-docstrings',
        'flake8-logging-format',
        'pep8-naming',
        'isort==4.3.10',
        'coverage',
        'codecov',
        'pylint',
    ]
}

TESTS_REQUIRE = [
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, 'mult_mixins', '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        logger.info(s)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')

        self.status('Pushing git tags...')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=(
        'contrib',
        'docs',
        'example',
    )),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    tests_require=TESTS_REQUIRE,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
    # $ setup.py test support
    test_suite="runtests.runtests",
)
