from django.urls import path
from .views import LoanCreateView, LoanYearlyAmortizationExportView, LoanApplyView, CustomerLoanListView, AdminPendingLoanListView

urlpatterns = [
    path("customer/create-loan/", LoanCreateView.as_view(), name="loan-create"),
    path("customer/apply/<int:pk>/", LoanApplyView.as_view(), name="loan-apply"),
    path("customer/list-loans/", CustomerLoanListView.as_view(), name="customer-loans"),
    path("admin/list-pending/", AdminPendingLoanListView.as_view(), name="admin-pending-loans"),
    path(
    "customer/yearly-schedule/export/<int:loan_id>/",
    LoanYearlyAmortizationExportView.as_view(),
    name="loan-yearly-export",
),
]