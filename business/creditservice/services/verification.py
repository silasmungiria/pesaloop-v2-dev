from datetime import datetime
from django.core.exceptions import ValidationError
from creditservice.models import CreditUser, Employer
from creditservice.utils import UserVerificationStatus

class VerificationService:
    @staticmethod
    def verify_employer(employer, verified_by):
        """Verify an employer and all their active employees"""
        if employer.is_verified:
            raise ValidationError("Employer is already verified")

        employer.is_verified = True
        employer.verified_by = verified_by
        employer.verified_at = datetime.now()
        employer.save()

        # Auto-verify all active employees
        CreditUser.objects.filter(
            employer=employer,
            verification_status=UserVerificationStatus.PENDING
        ).update(
            verification_status=UserVerificationStatus.VERIFIED,
            verified_by=verified_by,
            verified_at=datetime.now()
        )

        return employer

    @staticmethod
    def verify_employee(employee, verified_by):
        """Verify an individual employee"""
        if not employee.employer.is_verified:
            raise ValidationError("Employer must be verified first")

        if employee.verification_status == UserVerificationStatus.VERIFIED:
            raise ValidationError("Employee is already verified")

        employee.verification_status = UserVerificationStatus.VERIFIED
        employee.verified_by = verified_by
        employee.verified_at = datetime.now()
        employee.save()

        return employee
