from rest_framework import serializers
from ..models import Loan
from loans.utils.send_email import approval_email
import threading
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
        threading.Thread(target=approval_email, args=(loan,)).start()
        return loan
    