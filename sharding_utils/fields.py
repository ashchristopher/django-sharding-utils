from django.db import models


class ExternalIdField(models.BigIntegerField):
    """
    An id field which uses some external mechanism to populate the id.
    """
    def __init__(self, generate_id_callable=None, *args, **kwargs):
        super(ExternalIdField, self).__init__(*args, **kwargs)
        self.get_id = generate_id_callable

    def pre_save(self, model_instance, add):
        if not model_instance.pk:
            model_instance.id = self.get_id()
        return super(ExternalIdField, self).pre_save(model_instance, add)


class BigAutoField(models.BigIntegerField):
    """
    Auto increment field using a BigInteger instead of the regular Integer field.
    """
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'bigint AUTO_INCREMENT'
        if connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return 'bigserial'
        return super(BigAutoField, self).db_type(connection)


try:
    # if project is using South, then add the introspection rules
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^sharding_utils\.fields\.ExternalIdField"])
    add_introspection_rules([], ["^sharding_utils\.fields\.BigAutoField"])
except:
    pass
