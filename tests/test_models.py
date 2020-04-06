import importlib

import pytest
from django.db import models
from django.db import connection

from history_model.managers import HistoryManager
from .models import MyModel


class TestHistoryRecord:
    @pytest.mark.django_db
    def test_history_record_create_history_model(self):
        assert f'{MyModel._meta.db_table}history' in \
            connection.introspection.table_names()

    @pytest.mark.django_db
    def test_history_record_replaced_on_history_manager(self):
        assert isinstance(MyModel.history, HistoryManager)

    @pytest.mark.django_db
    def test_register_history_model_in_module_of_model(self):
        assert MyModel.__name__ in \
            dir(importlib.import_module(MyModel.__module__))

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'signal', (
            models.signals.class_prepared,
            models.signals.post_save,
            models.signals.post_delete
        )
    )
    def test_register_singnals_for_original_model(self, signal):
        assert bool(signal._live_receivers(MyModel))
