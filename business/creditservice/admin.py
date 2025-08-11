from django.contrib import admin
from django.utils import timezone
from datetime import timedelta

from .models import Employer, CreditUser, Loan, Repayment
from creditservice.services import LoanCalculator

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'is_verified', 'employee_count')
    list_filter = ('is_verified', 'industry')
    search_fields = ('name', 'registration_number', 'email')
    readonly_fields = ('created_at', 'updated_at', 'verified_at')
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'registration_number', 'tax_id', 'industry')
        }),
        ('Financial Information', {
            'fields': ('annual_revenue', 'employee_count')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone_number', 'email', 'website')
        }),
        ('Banking Details', {
            'fields': ('bank_name', 'bank_account', 'bank_branch')
        }),
        ('Payroll Information', {
            'fields': ('payroll_contact_name', 'payroll_contact_email', 'payroll_contact_phone')
        }),
        ('Verification Status', {
            'fields': ('is_verified', 'verified_by', 'verified_at')
        }),
    )

@admin.register(CreditUser)
class CreditUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer', 'monthly_salary', 'verification_status')
    list_filter = ('verification_status', 'employer')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    raw_id_fields = ('user', 'employer')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'disbursement_date', 'due_date', 'balance')
    list_filter = ('status', 'user__employer')
    search_fields = ('user__user__first_name', 'user__user__last_name', 'reference_number')
    readonly_fields = ('balance', 'is_overdue')
    actions = ['disburse_selected', 'cancel_selected']

    def disburse_selected(self, request, queryset):
        for loan in queryset.filter(status='approved'):
            loan.status = 'disbursed'
            loan.disbursement_date = timezone.now().date()
            loan.due_date = loan.disbursement_date + timedelta(days=30)
            loan.save()
            LoanCalculator.generate_repayment_schedule(loan)
    disburse_selected.short_description = "Disburse selected approved loans"

    def cancel_selected(self, request, queryset):
        for loan in queryset.filter(status__in=['pending', 'approved']):
            loan.cancel()
    cancel_selected.short_description = "Cancel selected pending/approved loans"

    def balance(self, obj):
        return obj.balance
    balance.short_description = 'Current Balance'

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Is Overdue'

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount_due', 'amount_paid', 'status', 'due_date')
    list_filter = ('status', 'loan__user__employer')
    search_fields = ('loan__user__user__first_name', 'reference_number')
    raw_id_fields = ('loan',)
