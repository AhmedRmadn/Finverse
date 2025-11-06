from rest_framework import serializers
from ..models import Loan
class LoanApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id"]

    def validate(self, data):
        loan = self.instance
        if loan.status != Loan.STATUS_DRAFT:
            raise serializers.ValidationError("Loan must be in draft state to apply.")
        return data

    def save(self, **kwargs):
        print("Applying for loan...")
        loan = self.instance
        loan.apply()  # round to 2 decimals
        print(loan)
        return loan