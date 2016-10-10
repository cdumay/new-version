#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""

from setuptools import setup, find_packages

setup(
    name='tat-new-version',
    version=open('VERSION', 'r').read().strip(),
    description="TAT versionning",
    long_description="",
    classifiers=["Programming Language :: Python", ],
    keywords='',
    author='Cedric DUMAY',
    author_email='cedric.dumay@gmail.com',
    url='https://github.com/cdumay/tat-new-version',
    license='Apache2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    install_requires=open('requirements.txt', 'r').read().strip(),
    entry_points="""
[console_scripts]
tat-new-version = tat_new_version:main
""",
)
