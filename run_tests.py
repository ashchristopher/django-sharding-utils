#!/usr/bin/env python
import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


_INSTALLED_APPS = (
    'sharding_utils',
)


_DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    },

    # Sharded databases.
    'shard_001': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    },
    'shard_002': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    },
    'shard_003': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    },

    # Feature partitioned databases
    'feature_A': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    },
    'feature_B': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    },
    'feature_C': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3'
    },
}


if not settings.configured:
    settings.configure(DATABASES=_DATABASES,INSTALLED_APPS=_INSTALLED_APPS)


def run_tests(*test_args):
    if not test_args:
        test_args = []

    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)



if __name__ == '__main__':
    run_tests()
