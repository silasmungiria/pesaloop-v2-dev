from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pesaloop.settings')

app = Celery('pesaloop')
app.conf.enable_utc = False
app.conf.update(timezone='Africa/Nairobi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # Data Encryption
    'data-encryption.rotate-key-monthly': {
        'task': 'data_encryption.services.KeyRotationService.rotate_encryption_key_monthly',
        'schedule': timedelta(days=30),
    },

    # AuthService
    'authservice.cleanup-expired-otps': {
        'task': 'authservice.notifications.tasks.cleanup_expired_otps',
        'schedule': timedelta(minutes=30),
    },

    # CreditService
    'creditservice.disburse-loans-hourly': {
        'task': 'creditservice.notifications.tasks.disburse_approved_loans_hourly',
        'schedule': timedelta(hours=1),
    },
    'creditservice.flag-overdues-12h': {
        'task': 'creditservice.notifications.tasks.flag_overdue_repayments',
        'schedule': timedelta(hours=12),
    },
    'creditservice.accrue-interest-daily': {
        'task': 'creditservice.notifications.tasks.accrue_daily_interest',
        'schedule': timedelta(days=1),
    },

    # PaymentService
    'paymentservice.send-reminders-17h': {
        'task': 'paymentservice.notifications.tasks.automated_reminders.send_queued_transaction_reminders',
        'schedule': timedelta(hours=17),
    },

    # # FraudService
    # 'fraudservice.batch-fraud-analysis': {
    #     'task': 'fraudservice.tasks.analyze_recent_transactions',
    #     'schedule': timedelta(minutes=30),
    # },
    # 'fraudservice.weekly-model-training': {
    #     'task': 'fraudservice.tasks.schedule_regular_model_training',
    #     'schedule': timedelta(days=7),
    # },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
