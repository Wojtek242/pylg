"""PyLg setup file."""

from codecs import open as codecs_open
from os import path

from setuptools import setup

PWD = path.abspath(path.dirname(__file__))

with codecs_open(path.join(PWD, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

INSTALL_REQUIRES = [
    'pyyaml',
]

EXTRAS_REQUIRE = {
    'dev': [
        'pytest',
        'pytest-cov',
    ]
}

setup(
    name='PyLg',
    version='1.3.3',
    description=('Python module to facilitate and automate the process of '
                 'writing runtime logs.'),
    long_description=LONG_DESCRIPTION,
    url='https://github.com/Wojtek242/pylg',

    author='Wojciech Kozlowski',
    author_email='wk@wojciechkozlowski.eu',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='development log debug trace',
    include_package_data=True,

    packages=["pylg"]

)
