# loans/models/bank_settings.py
from django.db import models
from decimal import Decimal

class BankSettings(models.Model):
    annual_interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("7.00"),
        help_text="Default annual interest rate (in %)"
    )
    late_fee_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("2.00"),
        help_text="Late fee percentage charged on overdue payments"
    )
    grace_period_days = models.PositiveIntegerField(
        default=10,
        help_text="Number of days allowed before late fee applies"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bank Settings"
        verbose_name_plural = "Bank Settings"

    def __str__(self):
        return f"Bank Settings (Rate: {self.annual_interest_rate}%)"

    @classmethod
    def get_settings(cls):
        """Always return a single settings object."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
