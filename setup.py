"""
GrapheneSanic
"""
import codecs
import os
import re

from setuptools import setup


def open_local(paths, mode='r', encoding='utf8'):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        *paths
    )

    return codecs.open(path, mode, encoding)


with open_local(['graphene_sanic', '__init__.py'], encoding='latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup_kwargs = {
    'name': 'graphene-sanic',
    'version': version,
    'url': 'https://github.com/ethe/graphene-sanic',
    'license': 'MIT',
    'author': 'Gwo',
    'author_email': 'lambda.guo@gmail.com',
    'description': (
        'A graphql web framework, combined graphene and sanic.'),
    'packages': ['graphene_sanic'],
    'platforms': 'any',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    'install_requires': [
        'sanic>=0.5.4',
        'graphene>=1.4'
    ]
}


setup(**setup_kwargs)
