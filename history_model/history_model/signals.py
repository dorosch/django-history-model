from django.db import models


class SignalDispatcher:
    @classmethod
    def register_signals(cls, sender):
        models.signals.class_prepared.connect(
            cls.class_prepared, sender=sender, weak=False
        )
        models.signals.post_save.connect(
            cls.post_save, sender=sender, weak=False
        )
        models.signals.post_delete.connect(
            cls.post_delete, sender=sender, weak=False
        )

    @staticmethod
    def class_prepared(sender, **kwargs):
        pass

    @staticmethod
    def post_save(instance, created, **kwargs):
        pass

    @staticmethod
    def post_delete(instance, **kwargs):
        pass
