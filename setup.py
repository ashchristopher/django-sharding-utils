import os
from setuptools import setup, find_packages
from sharding_utils import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-sharding-utils',
    version=__version__,
    packages = find_packages(),
    author='Ash Christopher',
    author_email='ash.christopher@gmail.com',
    description='TODO',
    license='LICENSE',
    url='https://github.com/ashchristopher/django-sharding-utils',
    keywords='django sharding partitioning shards multidb databases',
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    install_requires=[
        'Django>=1.4',
    ],
    tests_require=[
        'Django>=1.4', 'mock==1.0.1'
    ],
    test_suite='run_tests.run_tests',
)
