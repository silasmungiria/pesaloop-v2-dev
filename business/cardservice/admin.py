from django.contrib import admin
from .models import PaymentCard, Transaction

admin.site.register(PaymentCard)
admin.site.register(Transaction)
