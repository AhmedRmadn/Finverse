
from datetime import date
import calendar
from decimal import Decimal, getcontext
from django.utils import timezone

def first_of_next_month(d: date) -> date:
    year = d.year + (d.month // 12)
    month = (d.month % 12) + 1
    return date(year, month, 1)

def add_months(d: date, months: int) -> date:
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

def generate_amortization_schedule(loan):
    getcontext().prec = 28
    balance = loan.amount
    annual_rate = loan.annual_interest_rate
    r = annual_rate / Decimal("100") / Decimal("12") 
    n = int(loan.term_years) * 12
    M = loan.monthly_payment
    approved_date = timezone.now().date()
    first_due = first_of_next_month(approved_date)

    gap = (first_due - approved_date).days
    if gap < 10:
        first_due = first_of_next_month(first_due)  
    
    rows = []

    for i in range(1, n + 1):
        interest = (balance * r).quantize(Decimal("0.01"))
        principal = (M - interest).quantize(Decimal("0.01"))
        if i == n:
            principal = balance.quantize(Decimal("0.01"))
            M_last = (interest + principal).quantize(Decimal("0.01"))
        else:
            M_last = M

        balance = (balance - principal).quantize(Decimal("0.01"))

        due_date =add_months(first_due, i - 1) 

        rows.append(
            {
                "month_index" : i,
                "due_date" : due_date,
                "principal_component" : principal,
                "interest_component" :interest,
                "total_payment" : M_last,
            }
        )
    return rows