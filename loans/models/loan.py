from django.db import models
from django.conf import settings
from decimal import Decimal, getcontext
from django.utils import timezone
from datetime import date
import calendar
from django.db import transaction
from .loan_payment_schedule import LoanPaymentSchedule

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
    
    @staticmethod
    def _first_of_next_month(d: date) -> date:
        year = d.year + (d.month // 12)
        month = (d.month % 12) + 1
        return date(year, month, 1)

    @staticmethod
    def _add_months(d: date, months: int) -> date:
        month = d.month - 1 + months
        year = d.year + month // 12
        month = month % 12 + 1
        day = min(d.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    @transaction.atomic
    def approve(self, admin_user):
        self.status = self.STATUS_APPROVED
        self.approved_by = admin_user
        self.approved_at = timezone.now()
        self.save()

        getcontext().prec = 28
        P = self.amount
        annual_rate = self.annual_interest_rate
        r = annual_rate / Decimal("100") / Decimal("12") 
        n = int(self.term_years) * 12
        if r == 0:
            M = (P / Decimal(n)).quantize(Decimal("0.01"))
        else:
            M = (P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)).quantize(Decimal("0.01"))

        balance = P
        approved_date = timezone.now().date()
        first_due = self._first_of_next_month(approved_date)

        gap = (first_due - approved_date).days
        if gap < 10:
            first_due = self._first_of_next_month(first_due)  
        
        rows = []

        for i in range(1, n + 1):
            interest = (balance * r).quantize(Decimal("0.01"))
            principal = (M - interest).quantize(Decimal("0.01"))
            if i == n:
                principal = balance.quantize(Decimal("0.01"))
                M_last = (interest + principal).quantize(Decimal("0.01"))
            else:
                M_last = M

            balance = (balance - principal).quantize(Decimal("0.01"))

            due_date = self._add_months(first_due, i - 1) 

            rows.append(
                LoanPaymentSchedule(
                    loan=self,
                    user=self.created_by,
                    month_index=i,
                    due_date=due_date,
                    principal_component=principal,
                    interest_component=interest,
                    total_payment=M_last,
                    status=LoanPaymentSchedule.STATUS_PENDING,
                    late_fee_amount=Decimal("0.00"),
                )
            )
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

