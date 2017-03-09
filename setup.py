from setuptools import setup, find_packages
from codecs import open
from os import path

pwd = path.abspath(path.dirname(__file__))

with open(path.join(pwd, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyLg',
    version='1.2.0',
    description='Python module to facilitate and automate the process of writing runtime logs.',
    long_description=long_description,
    url='https://gitlab.wojciechkozlowski.eu/wojtek/PyLg',

    author='Wojciech Kozlowski',
    author_email='wojciech.kozlowski@vivaldi.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='development log debug trace',
    include_package_data=True,

    packages=["pylg"]

)
