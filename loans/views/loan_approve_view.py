from rest_framework import generics
from ..models import Loan
from ..serializers import  LoanApproveSerializer
from rest_framework.permissions import IsAdminUser

class LoanApproveView(generics.UpdateAPIView):
    serializer_class = LoanApproveSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Loan.objects.filter(status=Loan.STATUS_PENDING)