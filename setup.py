"""Install parameters for CLI and python import."""
from setuptools import setup

with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name='huber',
    version='0.4.0',
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
