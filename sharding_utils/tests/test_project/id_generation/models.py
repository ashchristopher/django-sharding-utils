from django.db import models

from . import generate_id
from sharding_utils.fields import ExternalIdField


class SimpleExternalIdFieldModel(models.Model):
    id = ExternalIdField(primary_key=True, generate_id_callable=generate_id)
