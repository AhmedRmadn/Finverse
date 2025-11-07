import csv
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from loans.models import Loan
from loans.utils.amortization_schedule import generate_amortization_schedule
from loans.utils.generate_style_sheet import export_amortization_excel


class LoanYearlyAmortizationExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id, created_by=request.user)

        schedule = generate_amortization_schedule(loan)
        wb = export_amortization_excel(loan, schedule)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response["Content-Disposition"] = f'attachment; filename="loan_{loan.id}_schedule.xlsx"'

        wb.save(response)
        return response
