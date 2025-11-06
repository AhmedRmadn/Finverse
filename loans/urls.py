from django.urls import path
from .views import LoanCreateView, LoanYearlyAmortizationExportView, LoanApplyView

urlpatterns = [
    path("customer/create-loan/", LoanCreateView.as_view(), name="loan-create"),
    path("customer/apply/<int:pk>/", LoanApplyView.as_view(), name="loan-apply"),
    path(
    "customer/yearly-schedule/export/<int:loan_id>/",
    LoanYearlyAmortizationExportView.as_view(),
    name="loan-yearly-export",
),
]