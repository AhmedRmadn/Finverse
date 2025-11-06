from django.urls import path
from .views import LoanCreateView

urlpatterns = [
    path("customer/create-loan/", LoanCreateView.as_view(), name="loan-create"),
]