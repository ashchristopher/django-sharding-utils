from mock import Mock

from django.test import TestCase

from sharding_utils.routers import BaseAppRouter


class AppRouterTestCase(TestCase):

    def test_can_not_instantiate_base_router(self):
        # should not be able to create an instance of BaseAppRouter
        self.assertRaises(AttributeError, BaseAppRouter)

    def test_can_not_instantiate_subclassed_router_with_missing_app_name(self):

        class TestRouter(BaseAppRouter):
            db_name = 'foo'

        with self.assertRaises(AttributeError):
            TestRouter()

    def test_can_not_instantiate_subclassed_router_with_missing_db_name(self):

        class TestRouter(BaseAppRouter):
            app_name = 'foo'

        with self.assertRaises(AttributeError):
            TestRouter()

    def test_can_not_instantiate_subclassed_router_missing_both_app_name_and_db_name(self):

        class TestRouter(BaseAppRouter):
            pass

        with self.assertRaises(AttributeError):
            TestRouter()


class AppRouterUsageTestCase(TestCase):

    def setUp(self):

        class Router(BaseAppRouter):
            app_name = 'test_app'
            db_name = 'test_db'
        self.router = Router()

    def test_db_for_read(self):
        model = Mock()
        model._meta.app_label = 'test_app'
        self.assertEquals(self.router.db_for_read(model), 'test_db')

    def test_db_for_read_different_apps(self):
        model = Mock()
        model._meta.app_label = 'other_app'
        self.assertIsNone(self.router.db_for_read(model))

    def test_db_for_write(self):
        model = Mock()
        model._meta.app_label = 'test_app'
        self.assertEquals(self.router.db_for_write(model), 'test_db')

    def test_db_for_write_different_apps(self):
        model = Mock()
        model._meta.app_label = 'other_app'
        self.assertIsNone(self.router.db_for_write(model))

    def test_allow_relation(self):
        model1 = Mock()
        model1._meta.app_label = 'test_app'

        model2 = Mock()
        model2._meta.app_label = 'test_app'

        self.assertTrue(self.router.allow_relation(model1, model2))
        self.assertTrue(self.router.allow_relation(model2, model1))

    def test_allow_relation_only_one_model_in_app(self):
        model1 = Mock()
        model1._meta.app_label = 'test_app'

        model2 = Mock()
        model2._meta.app_label = 'other_app'

        self.assertFalse(self.router.allow_relation(model1, model2))
        self.assertFalse(self.router.allow_relation(model2, model1))

    def test_allow_relation_neither_model_in_app(self):
        model1 = Mock()
        model1._meta.app_label = 'other_app'

        model2 = Mock()
        model2._meta.app_label = 'other_app'

        self.assertIsNone(self.router.allow_relation(model1, model2))
        self.assertIsNone(self.router.allow_relation(model2, model1))

    def test_allow_syncdb(self):
        model = Mock()
        model._meta.app_label = 'test_app'

        self.assertTrue(self.router.allow_syncdb('test_db', model))

    def test_allow_syncdb_in_other_db(self):
        model = Mock()
        model._meta.app_label = 'test_app'

        self.assertFalse(self.router.allow_syncdb('other_db', model))

    def test_allow_syncdb_model_in_other_app(self):
        model = Mock()
        model._meta.app_label = 'other_app'

        self.assertFalse(self.router.allow_syncdb('test_db', model))

    def test_allow_syncdb_model_in_other_app_and_other_db(self):
        model = Mock()
        model._meta.app_label = 'other_app'

        self.assertIsNone(self.router.allow_syncdb('other_db', model))

    def test_south_app_triggers_syncdb(self):
        model = Mock()
        model._meta.app_label = 'south'

        self.assertTrue(self.router.allow_syncdb('test_db', model))

    def test_south_app_triggers_syncdb_in_other_db(self):
        model = Mock()
        model._meta.app_label = 'south'

        self.assertIsNone(self.router.allow_syncdb('other_db', model))


