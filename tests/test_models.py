import importlib

import pytest
from django.db import models

from history_model.managers import HistoryManager


class TestHistoryRecord:
    @pytest.mark.django_db
    def test_create_history_model(self, history_model, db_tables):
        assert history_model._meta.db_table in db_tables

    @pytest.mark.django_db
    def test_history_record_replaced_on_history_manager(self, model):
        assert isinstance(model.history, HistoryManager)

    @pytest.mark.django_db
    def test_register_history_model_in_module_of_model(self, model):
        assert model.__name__ in \
            dir(importlib.import_module(model.__module__))

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'signal', (
            models.signals.post_save,
            models.signals.post_delete
        )
    )
    def test_register_singnals_for_original_model(self, signal, model):
        assert bool(signal._live_receivers(model))
