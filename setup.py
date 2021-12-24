#!/usr/bin/env python

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='nort',
    version='0.1.0',
    license='MIT',
    author='Max Schik',
    author_email='max.schik@googlemail.com',
    description='A tool for creating and managing notes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/taDachs/nort',
    packages=['nort'],
    data_files=[('share/nort', ['etc/nort.yaml'])],
    scripts=['scripts/nort'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['pyyaml'],
    python_requires='>=3.6',
)
