from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from .loan_payment_schedule import LoanPaymentSchedule
###import function generate_amortization_schedule from loans/utils/amortization_schedule.py
from loans.utils.amortization_schedule import generate_amortization_schedule

class Loan(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_ACTIVE = "active"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PENDING, "Pending Review"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_ACTIVE, "Active / In Payment"),
        (STATUS_FINISHED, "Finished / Paid"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loans"
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2)
    term_years = models.PositiveIntegerField()
    annual_interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("7.00")
    )

    monthly_payment = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    total_paid = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_late_fees = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    applied_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name="approved_loans",
        on_delete=models.SET_NULL
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_note = models.TextField(null=True, blank=True)


    def apply(self, monthly_payment):
        self.monthly_payment = monthly_payment
        self.status = self.STATUS_PENDING
        self.applied_at = timezone.now()
        self.save()
    
    @transaction.atomic
    def approve(self, admin_user):
        self.status = self.STATUS_APPROVED
        self.approved_by = admin_user
        self.approved_at = timezone.now()
        self.save()
        schedule_dicts = generate_amortization_schedule(self)

        rows = [
            LoanPaymentSchedule(
                loan=self,
                user=self.created_by,
                month_index=data["month_index"],
                due_date=data["due_date"],
                principal_component=data["principal_component"],
                interest_component=data["interest_component"],
                total_payment=data["total_payment"],
                status=LoanPaymentSchedule.STATUS_PENDING,
                late_fee_amount=Decimal("0.00"),
            )
            for data in schedule_dicts
        ]

        LoanPaymentSchedule.objects.bulk_create(rows)

    
    def reject(self, admin_user):
        self.status = self.STATUS_REJECTED
        self.rejected_by = admin_user
        self.rejected_at = timezone.now()
        self.save()
    def add_payment(self, amountToPay: Decimal, fee: Decimal = Decimal("0.00")):
        self.total_paid += amountToPay
        if fee > Decimal("0.00"):
            self.total_late_fees += fee
        if self.status == self.STATUS_APPROVED:
            self.status = self.STATUS_ACTIVE
        if self.total_paid >= self.amount:
            self.status = self.STATUS_FINISHED
        self.save()

    def __str__(self):
        return f"{self.created_by.username} - {self.amount} ({self.status})"

