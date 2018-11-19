# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os, sys, ast

here = os.path.abspath(os.path.dirname(__file__))

print(find_packages(exclude=['contrib', 'docs', 'tests', 'volatility_profile_builder.egg-info']))

#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
long_description = "See website for more info."

setup(
    name='volatility_profile_builder',
    version='0.0.1',
    description='Helper to build volatility profiles.',
    long_description=long_description,
    url='https://github.com/bannsec/volatility_profile_builder',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console'
    ],
    keywords='volatility profile build',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'volatility_profile_builder.egg-info']),
    install_requires=['requests', 'docker', 'prettytable'],
    entry_points={
        'console_scripts': [
            'volatility_profile_builder = volatility_profile_builder.volatility_profile_builder:main',
        ],
    },
    include_package_data=True,
)

