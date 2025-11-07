from rest_framework import serializers
from ..models import Loan
from loans.utils.send_email import rejection_email
import threading
class LoanRejectSerializer(serializers.ModelSerializer):
    admin_note = serializers.CharField(required=True)

    class Meta:
        model = Loan
        fields = ["id", "admin_note"]

    def validate(self, data):
        loan = self.instance
        if loan.status != Loan.STATUS_PENDING:
            raise serializers.ValidationError("Loan must be pending to reject.")
        return data

    def save(self, **kwargs):
        loan = self.instance
        admin_user = self.context["request"].user 
        loan.reject(admin_user)
        threading.Thread(target=rejection_email, args=(loan,)).start()
        return loan
