from django.urls import path
from .views import LoanCreateView, LoanYearlyAmortizationExportView

urlpatterns = [
    path("customer/create-loan/", LoanCreateView.as_view(), name="loan-create"),
    path(
    "customer/yearly-schedule/export/<int:loan_id>/",
    LoanYearlyAmortizationExportView.as_view(),
    name="loan-yearly-export",
),
]