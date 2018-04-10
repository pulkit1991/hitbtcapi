# coding: utf-8
import ast
import io
import os
import re
from setuptools import setup


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        if node.targets[0].id == '__version__':
            self.version = node.value.s


def read_version():
    """Read version without loading any files"""
    finder = VersionFinder()
    finder.visit(
        ast.parse(local_file('hitbtcapi', '__init__.py').encode('utf-8')))
    return finder.version


def parse_requirements(path):
    """Rudimentary parser for the `requirements.txt` file
    We just want to separate regular packages from links to pass them to the
    `install_requires` and `dependency_links` params of the `setup()`
    function properly.
    """
    try:
        requirements = [req.strip() for req in local_file(path).splitlines()]
    except IOError:
        raise RuntimeError("Could not find the `requirements.txt' file")

    links = []
    pkgs = []
    for req in requirements:
        if not req:
            continue
        if 'http:' in req or 'https:' in req:
            links.append(req)
            name, version = re.findall("\#egg=([^\-]+)-(.+$)", req)[0]
            pkgs.append('{}=={}'.format(name, version))
        else:
            pkgs.append(req)

    return pkgs, links


local_file = lambda *f: \
    io.open(
        os.path.join(os.path.dirname(__file__), *f), encoding='utf-8').read()


install_requires, dependency_links = \
    parse_requirements('requirements.txt')
tests_requires, tests_dependency_links = \
    parse_requirements('test-requirements.txt')



setup(
    name='hitbtcapi',
    version=read_version(),
    packages=['hitbtcapi'],
    description='HitBTC API Client library',
    long_description=local_file('README.rst'),
    author='Pulkit Gupta',
    author_email='gupta.pulkit91@gmail.com',
    url='https://github.com/pulkit1991/hitbtcapi',
    download_url='https://github.com/pulkit1991/hitbtcapi/tarball/%s' % read_version(),
    keywords=['hitbtc', 'api', 'client', 'bitcoin', 'altcoin', 'trading'],
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    test_suite='nose.collector',
    tests_require=tests_requires,
    license='MIT',
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
