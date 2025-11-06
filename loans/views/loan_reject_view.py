from rest_framework import generics
from ..models import Loan
from ..serializers import LoanRejectSerializer
from rest_framework.permissions import IsAdminUser


class LoanRejectView(generics.UpdateAPIView):
    serializer_class = LoanRejectSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Loan.objects.filter(status=Loan.STATUS_PENDING)

