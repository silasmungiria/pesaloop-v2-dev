from django.utils.translation import gettext_lazy as _

PERMISSION_CATEGORIES = [
    ('USER', _('User Management')),
    ('TRANSACTION', _('Transactions')),
    ('LOAN', _('Loan Operations')),
    ('REPORT', _('Reporting')),
    ('SYSTEM', _('System Administration')),
]

ROLE_LEVELS = [
    (1, _('Basic')),
    (2, _('Intermediate')),
    (3, _('Senior')),
    (4, _('Administrator')),
    (5, _('System')),
]
