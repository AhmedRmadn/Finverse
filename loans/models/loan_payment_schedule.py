from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone
from datetime import date
from django.db import transaction
class LoanPaymentSchedule(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_OVERDUE = "overdue"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_OVERDUE, "Overdue"),
    ]

    user = models.ForeignKey(               
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loan_payments"
    )

    loan = models.ForeignKey(
        "Loan",
        on_delete=models.CASCADE,
        related_name="schedule"
    )

    due_date = models.DateField()
    month_index = models.PositiveIntegerField()

    principal_component = models.DecimalField(max_digits=14, decimal_places=2)
    interest_component = models.DecimalField(max_digits=14, decimal_places=2)
    total_payment = models.DecimalField(max_digits=14, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    was_late = models.BooleanField(default=False)
    late_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"Loan {self.loan.id} - Month {self.month_index} ({self.status})"

@transaction.atomic
def mark_paid(self):
    today = date.today()
    if self.due_date > today:
        raise ValueError("Cannot pay in advance.")

    try:
        with transaction.atomic():
            self.status = self.STATUS_PAID
            self.paid_at = timezone.now()
            self.save()
            self.loan.add_payment(self.total_payment, self.late_fee_amount)
    except Exception as e:
        print(f"[ROLLBACK] Payment failed: {e}")
        raise 
    print("✅ Payment and loan updated successfully")