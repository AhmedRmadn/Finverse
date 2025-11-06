from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from ..models import  LoanPaymentSchedule
from ..serializers import LoanPaymentSerializer



class LoanPaymentView(generics.UpdateAPIView):
    serializer_class = LoanPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        payment_id = self.kwargs["pk"]
        return get_object_or_404(LoanPaymentSchedule, id=payment_id, user=user)