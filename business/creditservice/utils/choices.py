# creditservice/utils/choices.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class EmployerIndustry(models.TextChoices):
    TECHNOLOGY = 'technology', _('Technology')
    FINANCE = 'finance', _('Finance')
    HEALTHCARE = 'healthcare', _('Healthcare')
    EDUCATION = 'education', _('Education')
    MANUFACTURING = 'manufacturing', _('Manufacturing')
    RETAIL = 'retail', _('Retail')
    OTHER = 'other', _('Other')

class UserVerificationStatus(models.TextChoices):
    UNVERIFIED = 'unverified', _('Unverified')
    PENDING = 'pending', _('Pending Verification')
    VERIFIED = 'verified', _('Verified')
    REJECTED = 'rejected', _('Rejected')

class LoanStatus(models.TextChoices):
    PENDING = 'pending', _('Pending Approval')
    APPROVED = 'approved', _('Approved')
    DISBURSED = 'disbursed', _('Disbursed')
    PARTIAL = 'partial', _('Partial Payment')
    REPAID = 'repaid', _('Repaid')
    DEFAULTED = 'defaulted', _('Defaulted')
    RECONCILED = 'reconciled', _('Reconciled')

class RepaymentStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    PAID = 'paid', _('Paid')
    PARTIAL = 'partial', _('Partial Payment')
    OVERDUE = 'overdue', _('Overdue')
