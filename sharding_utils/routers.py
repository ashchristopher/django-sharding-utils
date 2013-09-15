class BaseAppRouter(object):
    """
    The AppBasedRouter class can be used to create a database router that partitions all data in
    a django application into it's own database.

    When subclassing the AppBasedRouter, you must provide `app_name` and `db_name` as class
    variables.

    eg:

        class FooBarRouter(AppBasedRouter):
            app_name = 'foo'
            db_name = 'bar'

    """

    def __init__(self, *args, **kwargs):
        if not (self.app_name or self.db_name):
            raise AttributeError('Router missing both class variables `app_name` and `db_name`')

        if not self.app_name:
            raise AttributeError('Router missing class variable `app_name`')

        if not self.db_name:
            raise AttributeError('Router missing class variable `db_name`')

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_name:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_name:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # we only want to allow joins between objects in the same app
        if obj1._meta.app_label == self.app_name and obj2._meta.app_label == self.app_name:
            # if both of the models are from the app, then we can allow relations.
            return True

        elif obj1._meta.app_label == self.app_name or obj2._meta.app_label == self.app_name:
            # if only one of the models are from the app, then we explicitly DO NOT allow relations.
            return False
        else:
            # if neither of the models are from the app, then we have no opinion.
            return None

    def allow_syncdb(self, db, model):
        if db == self.db_name:

            if model._meta.app_label in ['south', ]:
                return True

            if db == self.db_name:
                return model._meta.app_label == self.app_name

        return None


class BaseMultiAppRouter(object):
    """
    The MultiAppBasedRouter class can be used to create a database router that partitions all
    data based on multiple applications.

    By partitioning based on many apps, all the apps in the `app_list` can maintain their
    foreign keys.

    When subclassing the MultiAppBasedRouter, you must provide an `app_list` iterable and
    `db_name` as class variables.

    eg:

        class FooBarRouter(AppBasedRouter):
            app_list = ['foo', 'bar', 'baz', ]
            db_name = 'my_database'

    """

    def __init__(self, *args, **kwargs):
        if not (self.app_list or self.db_name):
            raise AttributeError('Router missing both class variables `app_list` and `db_name`')

        if not self.app_list:
            raise AttributeError('Router missing class variable `app_list`')

        if not self.db_name:
            raise AttributeError('Router missing class variable `db_name`')

        valid_app_list = isinstance(self.app_list, list) or isinstance(self.app_list, tuple)

        if not valid_app_list:
            raise AttributeError('Router class variable `app_list` must be of type `list`')

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_list:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_list:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # we only want to allow joins between objects that come from apps in the list
        if obj1._meta.app_label in self.app_list and obj2._meta.app_label in self.app_list:
            # if both of the models are from the apps in the list, then we can allow relations.
            return True

        elif obj1._meta.app_label in self.app_list or obj2._meta.app_label in self.app_list:
            # if only one of the models are from apps in the list, then we explicitly DO NOT allow relations.
            return False
        else:
            # if neither of the models are from apps in the list, then we have no opinion.
            return None

    def allow_syncdb(self, db, model):
        if model._meta.app_label in ['south']:
            return True

        if db == self.db_name:
            return model._meta.app_label in self.app_list
        return None


class BaseShardRouter(object):
    """
    Base class for routers allowing several apps to be grouped in a shard group.

    Subclasses need to define a list of app names and a prefix for the db names of the shard group.

    e.g.,

    app_list = ('my_app1', )
    db_names_prefix = 'my_shard_'

    """

    app_list = tuple()
    db_name_prefix = None

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_list:
            instance = hints.get('instance')
            if instance:
                return instance.get_shard()
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_list:
            instance = hints.get('instance')
            if instance:
                return instance.get_shard()
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # we only want to allow joins between objects that come from apps in the list
        if obj1._meta.app_label in self.app_list and obj2._meta.app_label in self.app_list:
            # if both of the models are from the apps in the list, then we can allow relations.
            return True

        elif obj1._meta.app_label in self.app_list or obj2._meta.app_label in self.app_list:
            # if only one of the models are from apps in the list, then we explicitly DO NOT allow relations.
            return False
        else:
            # if neither of the models are from apps in the list, then we have no opinion.
            return None

    def allow_syncdb(self, db, model):
        if model._meta.app_label in ['south']:
            return True

        # logic was pulled from: https://github.com/malcolmt/django-multidb-patterns/blob/master/sharding/reviews/router.py#L22
        this_app = (model._meta.app_label in self.app_list)
        _db = db.startswith(self.db_names_prefix)
        if this_app:
            return _db
        if _db:
            return False
        return None
