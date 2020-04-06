import importlib

from django.db import models

from .signals import SignalDispatcher
from .managers import HistoryDescriptor


class HistoryModel:
    def __init__(self, original_model):
        self.model = original_model
        self.bases = (models.Model,)
        self.name = f'{self.model._meta.object_name}History'
        self.attrs = {
            '__module__': self.model.__module__,
            **{field.name: field for field in self.model._meta.fields}
        }

    def create(self):
        return type(self.name, self.bases, self.attrs)


class HistoryRecord:
    @staticmethod
    def contribute_to_class(original_model, name):
        # Create history model as <ModelName>History
        history_model = HistoryModel(original_model).create()

        # Replace field HistoryRecord with the historical model manager
        descriptor = HistoryDescriptor(history_model)
        setattr(original_model, name, descriptor)

        # Register the model in module space so that migrations
        # for the historical model can be created
        module = importlib.import_module(original_model.__module__)
        setattr(module, history_model.__name__, history_model)

        # Register signals for records of the original model
        SignalDispatcher.register_signals(original_model)
