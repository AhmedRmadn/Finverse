from django.core.mail import send_mail
from django.conf import settings
def approval_email(loan):
    subject="Your Loan Has Been Approved ✅"
    message=(
            f"Hello {loan.created_by.first_name},\n\n"
            f"Your loan request for {loan.amount} has been approved.\n"
            f"Monthly Payment: {loan.monthly_payment}\n"
            f"Status: Approved\n\n"
            f"Thank you for banking with us!"
        )
    from_email=settings.DEFAULT_FROM_EMAIL
    recipient_list=[loan.created_by.email]
    fail_silently=False,
    send_mail(subject, message, from_email, recipient_list, fail_silently)
def rejection_email(loan):
    subject="Your Loan Has Been Rejected ❌"
    message=(
            f"Hello {loan.created_by.first_name},\n\n"
            f"We regret to inform you that your loan request for {loan.amount} has been rejected.\n"
            f"Status: Rejected\n\n"
            f"Please contact support for more information."
        )
    from_email=settings.DEFAULT_FROM_EMAIL
    recipient_list=[loan.created_by.email]
    fail_silently=False,
    send_mail(subject, message, from_email, recipient_list, fail_silently)

