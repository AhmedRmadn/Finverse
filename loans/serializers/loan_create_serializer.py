from rest_framework import serializers
from ..models import Loan, BankSettings
from loans.utils.monthly_payment import calc_monthly_payment


class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "amount", "term_years"]

    def create(self, validated_data):
        settings = BankSettings.get_settings()
        annual_rate = settings.annual_interest_rate
        user = self.context["request"].user
        amount=validated_data["amount"]
        term_years=validated_data["term_years"]
        monthly_payment = calc_monthly_payment(amount, annual_rate, term_years)
        return Loan.objects.create(
            created_by=user,
            amount= amount,
            term_years= term_years,
            annual_interest_rate= annual_rate,
            monthly_payment= monthly_payment,
            status=Loan.STATUS_DRAFT
        )