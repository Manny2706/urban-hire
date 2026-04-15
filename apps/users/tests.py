from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta


class CustomerAuthAPITests(APITestCase):
	def test_customer_signup_returns_tokens(self):
		url = reverse('customer-signup')
		payload = {
			'username': 'johncustomer',
			'email': 'john@example.com',
			'first_name': 'John',
			'last_name': 'Doe',
			'password': 'StrongPass123!',
			'confirm_password': 'StrongPass123!',
		}

		response = self.client.post(url, payload, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('tokens', response.data)
		self.assertIn('access', response.data['tokens'])
		self.assertIn('refresh', response.data['tokens'])
		self.assertTrue(User.objects.filter(username='johncustomer').exists())

	def test_customer_logout_blacklists_refresh_token(self):
		user = User.objects.create_user(
			username='logoutcustomer',
			email='logout@example.com',
			password='StrongPass123!',
		)
		refresh = RefreshToken.for_user(user)
		url = reverse('customer-logout')

		response = self.client.post(url, {'refresh': str(refresh)}, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], 'Customer logged out successfully.')
		self.assertTrue(BlacklistedToken.objects.filter(token__jti=refresh['jti']).exists())

	def test_customer_logout_rejects_expired_refresh_token(self):
		user = User.objects.create_user(
			username='expiredcustomer',
			email='expired@example.com',
			password='StrongPass123!',
		)
		refresh = RefreshToken.for_user(user)
		refresh.set_exp(lifetime=timedelta(seconds=-1))
		url = reverse('customer-logout')

		response = self.client.post(url, {'refresh': str(refresh)}, format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('refresh', response.data)
		self.assertEqual(str(response.data['refresh']), 'Refresh token is invalid or expired.')

	def test_customer_login_returns_tokens(self):
		User.objects.create_user(
			username='janecustomer',
			email='jane@example.com',
			password='StrongPass123!',
		)
		url = reverse('customer-login')
		payload = {
			'username': 'janecustomer',
			'password': 'StrongPass123!',
		}

		response = self.client.post(url, payload, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)
		self.assertIn('refresh', response.data)
