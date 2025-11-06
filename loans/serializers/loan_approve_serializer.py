from rest_framework import serializers
from ..models import Loan
class LoanApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id"]

    def validate(self, data):
        loan = self.instance
        if loan.status != Loan.STATUS_PENDING:
            raise serializers.ValidationError("Loan must be pending to approve.")
        return data

    def save(self, **kwargs):
        loan = self.instance
        admin_user = self.context["request"].user 
        loan.approve(admin_user)  
        return loan
    