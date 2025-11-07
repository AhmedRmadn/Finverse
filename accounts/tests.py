from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class AuthTests(APITestCase):

    def test_register_user(self):
        data = {
            "username": "testuser",
            "password": "123456",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@mail.com"
        }
        url = reverse("register")  # ✅ now works
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_user(self):
        User.objects.create_user(username="loginuser", password="pass123")
        data = {"username": "loginuser", "password": "pass123"}
        url = reverse("login")  # ✅ matches your URL name
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
