from rest_framework import generics, permissions
from ..serializers import LoanCreateSerializer
class LoanCreateView(generics.CreateAPIView):
    serializer_class = LoanCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

