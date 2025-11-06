from rest_framework import serializers
from ..models import LoanPaymentSchedule
from django.utils import timezone

class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPaymentSchedule
        fields = ["id", "month_index", "due_date", "status", "total_payment"]

    def validate(self, data):
        payment = self.instance
        today = timezone.now().date()

        if payment.due_date > today:
            raise serializers.ValidationError("You cannot pay in advance.")
        if payment.status == LoanPaymentSchedule.STATUS_PAID:
            raise serializers.ValidationError("This installment is already paid.")
        return data

    def save(self, **kwargs):
        payment = self.instance
        payment.mark_paid()
        return payment