from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class ItemTestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Generate a JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Set the token in the request header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_read_item(self):
        url = reverse('item-list-create')  # Ensure this matches your actual URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
