from django.db import models

from history_model.models import HistoryRecord


class Spam(models.Model):
    name = models.CharField(
        max_length=32
    )


class Poll(models.Model):
    spam = models.ForeignKey(
        to=Spam,
        on_delete=models.CASCADE
    )

    history = HistoryRecord()
