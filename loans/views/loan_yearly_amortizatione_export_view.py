import csv
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from loans.models import Loan
from loans.utils.amortization_schedule import generate_amortization_schedule


class LoanYearlyAmortizationExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id, created_by=request.user)

        # 🔹 Generate amortization schedule dynamically
        schedule = generate_amortization_schedule(loan)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="loan_{loan.id}_yearly_schedule.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Year",
            "Cumulative Interest",
            "Cumulative Principal",
            "Balance",
            "Cumulative Payments",
            "Yearly Payments",
            "Yearly Interest",
        ])

        cumulative_interest = Decimal("0.00")
        cumulative_principal = Decimal("0.00")
        cumulative_payments = Decimal("0.00")
        balance = loan.amount
        n = loan.term_years

        # 🔹 Aggregate dynamically per year
        for year in range(1, n + 1):
            year_rows = schedule[(year - 1) * 12: year * 12]

            yearly_interest = sum([r["interest_component"] for r in year_rows], Decimal("0.00"))
            yearly_principal = sum([r["principal_component"] for r in year_rows], Decimal("0.00"))
            yearly_payment = sum([r["total_payment"] for r in year_rows], Decimal("0.00"))

            cumulative_interest += yearly_interest
            cumulative_principal += yearly_principal
            cumulative_payments += yearly_payment
            balance = loan.amount - cumulative_principal

            writer.writerow([
                year,
                f"{cumulative_interest:.2f}",
                f"{cumulative_principal:.2f}",
                f"{balance:.2f}",
                f"{cumulative_payments:.2f}",
                f"{yearly_principal:.2f}",
                f"{yearly_interest:.2f}",
            ])

        return response
