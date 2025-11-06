from decimal import Decimal, getcontext
def calc_monthly_payment(amount: Decimal, annual_rate: Decimal, term_years: int) -> Decimal:
    getcontext().prec = 28
    P = amount
    r = annual_rate / Decimal("100") / Decimal("12")  
    n = term_years * 12

    if r == 0:
        M = (P / Decimal(n)).quantize(Decimal("0.01"))
    else:
        M = (P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)).quantize(Decimal("0.01"))

    return M
