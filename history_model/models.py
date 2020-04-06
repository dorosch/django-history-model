import importlib

from django.db import models

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
    def __init__(self):
        self.manager_name = None

    def contribute_to_class(self, original_model, name):
        # Save field of history manager
        self.manager_name = name

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
        models.signals.post_save.connect(
            self.post_save, sender=original_model, weak=False
        )
        models.signals.post_delete.connect(
            self.post_delete, sender=original_model, weak=False
        )

    def post_save(self, instance, created, **kwargs):
        attrs = {
            field.attname: getattr(instance, field.attname)
            for field in instance._meta.fields
        }
        manager = getattr(instance, self.manager_name)

        if created:
            # TODO: Added if instance is updated
            manager.model(**attrs).save(using=kwargs.get('using'))

    def post_delete(self, instance, **kwargs):
        manager = getattr(instance, self.manager_name)
        manager.model.objects.filter(pk=instance.pk).delete()
