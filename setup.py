#!/usr/bin/env python

from setuptools import setup

setup(
        name='igrep',
        version='0.9.1',
        description='Find image files by attributes like dimension and aspect ratio.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            ],
        install_requires=[
            'PIL',
            'ImageUtils',
            'ScriptUtils',
            ],
        entry_points={
            'console_scripts': [
                'igrep=igrep:main',
                ]
            },
        py_modules=[
            'igrep',
            ],
        )
