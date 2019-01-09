#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""

from setuptools import setup, find_packages

setup(
    name='tat-pytools',
    version=open('VERSION', 'r').read().strip(),
    description="TAT python tools",
    long_description="",
    classifiers=["Programming Language :: Python", ],
    keywords='',
    author='Cedric DUMAY',
    author_email='cedric.dumay@gmail.com',
    url='https://github.com/cdumay/tat-pytools',
    license='Apache2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    install_requires=open('requirements.txt', 'r').read().strip(),
    entry_points="""
[console_scripts]
tat-new-version = tat_pytools.new_version:new
tat-push-version = tat_pytools.new_version:current
tat-message = tat_pytools.message:main
commit-msg = tat_pytools.commit_hook:main
tat-annonce = tat_pytools.annonce:main
release-display = tat_pytools.release:main
release-current = tat_pytools.release:last
""",
)
