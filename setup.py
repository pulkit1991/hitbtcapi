# coding: utf-8
import os
from setuptools import setup
import hitbtcapi

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

REQUIREMENTS = [line.strip() for line in open(os.path.join(os.path.dirname(__file__),'requirements.txt')).readlines()]

setup(
    name='hitbtcapi',
    version=hitbtcapi.__version__,
    packages=['hitbtcapi'],
    include_package_data=True,
    license='MIT',
    description='HitBTC API Client library',
    long_description=README,
    url='https://github.com/pulkit1991/hitbtcapi/',
    download_url='https://github.com/pulkit1991/hitbtcapi/tarball/%s' % (
      hitbtcapi.__version__),
    keywords=['hitbtc', 'api', 'client', 'bitcoin', 'altcoin', 'trading'],
    install_requires=REQUIREMENTS,
    author='Pulkit Gupta',
    author_email='gupta.pulkit91@gmail.com',
    classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
