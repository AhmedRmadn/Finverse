from rest_framework import generics
from ..models import Loan
from ..serializers import LoanListSerializer
from rest_framework.permissions import IsAdminUser
class AdminPendingLoanListView(generics.ListAPIView):
    serializer_class = LoanListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Loan.objects.filter(status=Loan.STATUS_PENDING).order_by("-applied_at")