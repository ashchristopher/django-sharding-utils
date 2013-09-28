from django.db.models.fields import BigIntegerField


class BigAutoField(BigIntegerField):
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
    add_introspection_rules([], ["^sharding_utils\.fields\.BigAutoField"])
except:
    pass
