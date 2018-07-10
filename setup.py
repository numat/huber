"""Install parameters for CLI and python import."""
from setuptools import setup

setup(
    name='huber',
    version='0.2.4',
    description='Python driver for Huber recirculating baths.',
    url='http://github.com/numat/huber/',
    author='Patrick Fuller',
    author_email='pat@numat-tech.com',
    packages=['huber'],
    entry_points={
        'console_scripts': [('huber = huber:command_line')]
    },
    license='GPLv2',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ]
)
