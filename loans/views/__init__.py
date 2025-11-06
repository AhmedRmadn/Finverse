from .loan_create_view import LoanCreateView
from .loan_yearly_amortizatione_export_view import LoanYearlyAmortizationExportView
from .loan_apply_view import LoanApplyView
from .customer_loan_list_view import CustomerLoanListView
from .admin_pending_loan_list_view import AdminPendingLoanListView
from .loan_approve_view import LoanApproveView
from .loan_reject_view import LoanRejectView
from .loan_payment_view import LoanPaymentView
__all__ = ["LoanCreateView", "LoanYearlyAmortizationExportView", 
           "LoanApplyView", "CustomerLoanListView", "AdminPendingLoanListView",
           "LoanApproveView","LoanRejectView", "LoanPaymentView"
           ]