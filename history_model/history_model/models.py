import importlib

from django.db import models

from .manager import HistoryDescriptor


class HistoryRecord:
    def contribute_to_class(self, model, name):
        history_model = self.create_history_model(model)

        module = importlib.import_module(model.__module__)
        setattr(module, history_model.__name__, history_model)

        descriptor = HistoryDescriptor(history_model)
        setattr(model, name, descriptor)

        # TODO: Added class_prepared signal
        models.signals.post_save.connect(
            self.post_save, sender=model, weak=False
        )

    def post_save(self, instance, created, **kwargs):
        pass

    def create_history_model(self, model):
        name = self.get_history_model_name(model)
        bases = self.get_bases_classes()
        attrs = self.get_attrs_history_model(model)
        return type(name, bases, attrs)

    @staticmethod
    def get_history_model_name(model):
        return f'{model._meta.object_name}History'

    @staticmethod
    def get_bases_classes():
        return models.Model,

    @staticmethod
    def get_attrs_history_model(model):
        return {
            '__module__': model.__module__,
            **{field.name: field for field in model._meta.fields}
        }
