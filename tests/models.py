from django.db import models

from history_model import models as history_models


class MyModel(models.Model):
    history = history_models.HistoryRecord()
