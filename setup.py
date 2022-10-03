"""Install parameters for CLI and python import."""
from sys import version_info
from setuptools import setup


if version_info < (3, 7):
    raise ImportError("This module requires Python >=3.7 for asyncio support")

with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name='huber',
    version='0.5.0',
    description='Python driver for Huber recirculating baths.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/numat/huber/',
    author='Patrick Fuller',
    author_email='pat@numat-tech.com',
    packages=['huber'],
    package_data={'huber': ['faults.csv']},
    entry_points={
        'console_scripts': [('huber = huber:command_line')]
    },
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
            'flake8>=3,<6',
            'flake8-docstrings==1.*',
        ],
    },
    license='GPLv2',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ]
)
