from rest_framework import serializers
from ..models import Loan
class LoanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "amount",
            "term_years",
            "annual_interest_rate",
            "monthly_payment",
            "status",
            "created_at",
            "applied_at"
        ]