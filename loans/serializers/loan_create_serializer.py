from rest_framework import serializers
from ..models import Loan


class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "amount", "term_years"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Loan.objects.create(
            created_by=user,
            amount=validated_data["amount"],
            term_years=validated_data["term_years"],
            status=Loan.STATUS_DRAFT
        )