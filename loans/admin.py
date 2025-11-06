from django.contrib import admin
from .models import Loan, LoanPaymentSchedule


# Register your models here.
admin.site.register(Loan)
admin.site.register(LoanPaymentSchedule)