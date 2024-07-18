#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup
from os import system

version = '1.0.1'

setup(
    name='jutge-server-toolkit',
    packages=['jutge.servertoolkit'],
    install_requires=[
        'jutge-toolkit',
    ],
    version=version,
    description='Server Toolkit for Jutge.org',
    long_description='Server Toolkit for Jutge.org',
    author='Jordi Petit et al',
    author_email='jpetit@cs.upc.edu',
    url='https://github.com/jutge-org/jutge-server-toolkit',
    download_url='https://github.com/jutge-org/jutge-server-toolkit/tarball/{}'.format(version),
    keywords=['jutge', 'jutge.org', 'education', 'toolkit'],
    license='Apache',
    zip_safe=False,
    include_package_data=True,
    setup_requires=['setuptools'],
    entry_points={
        'console_scripts': [
        ]
    },
    scripts=[
        'scripts/jutge-run',
        'scripts/jutge-submit',
        'scripts/jutge-install-sudo-tools',
    ]
)
