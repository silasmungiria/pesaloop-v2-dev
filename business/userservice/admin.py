from django.contrib import admin
from .models import User, Customer, Merchant, ActivityTrail

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Merchant)
admin.site.register(ActivityTrail)
