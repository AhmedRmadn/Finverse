from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from loans.models import Loan

class LoanTests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(username="cust", password="123")
        self.admin = User.objects.create_user(username="admin", password="123", is_staff=True)

    def auth(self, user):
        url = reverse("login")
        response = self.client.post(url, {"username": user.username, "password": "123"})
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_customer_can_create_loan(self):
        self.auth(self.customer)
        url = reverse("loan-create")
        response = self.client.post(url, {"amount": "100000", "term_years": 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)

    def test_customer_can_apply_for_loan(self):
        self.auth(self.customer)
        loan = Loan.objects.create(created_by=self.customer, amount=100000, term_years=10)
        url = reverse("loan-apply", args=[loan.id])
        response = self.client.patch(url)
        loan.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(loan.status, Loan.STATUS_PENDING)

    def test_admin_can_approve_loan(self):
        loan = Loan.objects.create(created_by=self.customer, monthly_payment=2000, amount=100000, term_years=10, status=Loan.STATUS_PENDING)
        self.auth(self.admin)
        url = reverse("loan-approve", args=[loan.id])
        response = self.client.patch(url)
        loan.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(loan.status, Loan.STATUS_APPROVED)

    def test_customer_cannot_approve_loan(self):
        loan = Loan.objects.create(created_by=self.customer, amount=100000, term_years=10, status=Loan.STATUS_PENDING)
        self.auth(self.customer)
        url = reverse("loan-approve", args=[loan.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
