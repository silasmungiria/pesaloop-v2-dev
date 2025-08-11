# Customer Document Types
class CustomerDocType:
    NATIONAL_ID = 'national_id'
    PASSPORT = 'passport'
    DRIVING_LICENSE = 'driving_license'
    CHOICES = [
        (NATIONAL_ID, 'National ID'),
        (PASSPORT, 'Passport'),
        (DRIVING_LICENSE, 'Driving License'),
    ]


# Customer Verification Status
class CustomerStatus:
    PARTIAL_SUBMISSION = 'partial_submission'
    UNDER_REVIEW = 'under_review'
    VERIFIED = 'verified'
    REQUIRES_ATTENTION = 'requires_attention'
    PERIODIC_REVIEW = 'periodic_review'
    CHOICES = [
        (PARTIAL_SUBMISSION, 'Partial Submission'),
        (UNDER_REVIEW, 'Under Review'),
        (VERIFIED, 'Verified'),
        (REQUIRES_ATTENTION, 'Verification Requires Attention'),
        (PERIODIC_REVIEW, 'Periodic Review Required'),
    ]


# Settlement Schedule Choices
class SettlementSchedule:
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    ]
