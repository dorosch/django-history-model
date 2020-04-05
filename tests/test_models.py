import pytest
from django.db import connection

from history_model.manager import HistoryManager
from .models import MyModel


class TestHistoryRecord:
    @pytest.mark.django_db
    def test_history_record_create_history_model(self):
        assert f'{MyModel._meta.db_table}history' in \
            connection.introspection.table_names()

    @pytest.mark.django_db
    def test_history_record_replaced_on_history_manager(self):
        assert isinstance(MyModel.history, HistoryManager)
