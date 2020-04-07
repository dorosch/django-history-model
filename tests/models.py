from django.db import models

from history_model import models as history_models


class MyModel(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    history = history_models.HistoryRecord()
