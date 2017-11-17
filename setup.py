"""
To make release:
    python setup.py sdist
Installation:
    python setup.py install
"""
import sys
import os
from distutils.core import setup
from setuptools import find_packages


data_files = [
    (
        'templates',
        [
            os.path.join('templates', name)
            for name in os.listdir('templates')
        ]
    )
]


setup(
    name='pypacker',
    version='1.0',
    packages=find_packages(),
    data_files=data_files,
    scripts=['pypacker-apply.py'],
)
