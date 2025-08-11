from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .base import BaseModel
from creditservice.utils import EmployerIndustry

User = get_user_model()

class Employer(BaseModel):
    # Company Identification
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, unique=True)
    tax_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    industry = models.CharField(max_length=100, choices=EmployerIndustry.choices)

    # Financial Information
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    employee_count = models.PositiveIntegerField(null=True, blank=True)

    # Contact Information
    address = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True, null=True)

    # Verification Status
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='verified_employers')
    verified_at = models.DateTimeField(null=True, blank=True)

    # Banking Details
    bank_name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=50)
    bank_branch = models.CharField(max_length=100)

    # Payroll Information
    payroll_contact_name = models.CharField(max_length=255)
    payroll_contact_email = models.EmailField()
    payroll_contact_phone = models.CharField(validators=[phone_regex], max_length=17)

    # Metadata
    external_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Employer"
        verbose_name_plural = "Employers"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.registration_number})"
