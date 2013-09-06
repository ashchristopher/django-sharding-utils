import os
from setuptools import setup, find_packages


VERSION = '0.0.1'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-sharding-utils',
    version='0.0.1',
    packages = find_packages(),
    author='Ash Christopher',
    author_email='ash.christopher@gmail.com',
    description='TODO',
    license='LICENSE',
    url='https://github.com/ashchristopher/django-sharding-utils',
    keywords='django sharding partitioning shards multidb databases',
    long_description=read('README.md'),
)
