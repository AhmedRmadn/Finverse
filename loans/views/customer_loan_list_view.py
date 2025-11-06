from rest_framework import generics, permissions
from ..models import Loan
from ..serializers import LoanListSerializer
class CustomerLoanListView(generics.ListAPIView):
    serializer_class = LoanListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(created_by=self.request.user).order_by("-created_at")