from django.contrib import admin
from . import models as forex_models

admin.site.register(forex_models.RateSnapshot)
admin.site.register(forex_models.CurrencyExchangeRecord)
