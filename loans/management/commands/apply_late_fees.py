from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from loans.models.loan_payment_schedule import LoanPaymentSchedule
from loans.models.bank_settings import BankSettings
from datetime import timedelta

class Command(BaseCommand):
    help = "Apply late fees and mark overdue loan payments"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        settings = BankSettings.get_settings()
        late_fee_rate = settings.late_fee_rate
        grace_period = settings.grace_period_days

        overdue_payments = LoanPaymentSchedule.objects.filter(
            status=LoanPaymentSchedule.STATUS_PENDING,
            due_date__lt=today - timedelta(days=grace_period)
        )

        self.stdout.write(f"Found {overdue_payments.count()} overdue payments to process")

        for payment in overdue_payments:
            months_overdue = max(1, (today.year - payment.due_date.year) * 12 + (today.month - payment.due_date.month))
            base_fee = (payment.total_payment * late_fee_rate / Decimal("100")).quantize(Decimal("0.01"))
            total_fee = (base_fee * months_overdue).quantize(Decimal("0.01"))
            payment.late_fee_amount += total_fee
            payment.status = LoanPaymentSchedule.STATUS_OVERDUE
            payment.save(update_fields=["late_fee_amount", "status", "updated_at"])
            self.stdout.write(f"Updated payment {payment.id}: +{total_fee} (months overdue={months_overdue})")

        self.stdout.write(self.style.SUCCESS("Late fee application completed."))
