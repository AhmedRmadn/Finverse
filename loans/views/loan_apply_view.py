from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from ..models import Loan
from ..serializers import LoanApplySerializer


class LoanApplyView(generics.UpdateAPIView):
    serializer_class = LoanApplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        loan_id = self.kwargs["pk"]
        loan = get_object_or_404(Loan, id=loan_id, created_by=self.request.user)
        return loan
    