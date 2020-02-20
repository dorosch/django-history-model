from django.db import models

from .manager import HistoryDescriptor


class HistoryRecord:
    def __init__(self, verbose_name=None, exclude_fields=None):
        self.verbose_name = verbose_name
        self.exclude_fields = exclude_fields

    def contribute_to_class(self, model, name):
        history_model = self.create_history_model(model)

        descriptor = HistoryDescriptor(history_model)
        setattr(model, name, descriptor)

        models.signals.post_save.connect(
            self.post_save, sender=model, weak=False
        )

    def post_save(self, instance, created, **kwargs):
        pass

    def create_history_model(self, model):
        return model
