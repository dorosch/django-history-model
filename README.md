# django-history-model

The easiest way to create a history models for django


## Installation

Install using `pip`...

    pip install django-history-model


## Example

Add `'history_model'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = [
        ...
        'history_model',
    ]

And just use:

```python
from django.db import models
from history_model.models import HistoryRecord

class YourModel(models.Model):
    history = HistoryRecord()
```
