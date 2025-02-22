from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from restaurant.models import Menu, Booking
from restaurant.serializers import MenuItemSerializer, BookingSerializer
from decimal import Decimal
from django.utils import timezone
from rest_framework.authtoken.models import Token

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.menu1 = Menu.objects.create(
            title="Pizza",
            price=Decimal('12.99'),
            inventory=50
        )
        self.menu2 = Menu.objects.create(
            title="Burger",
            price=Decimal('8.99'),
            inventory=30
        )
    
    def test_getall(self):
        """Test retrieving all menu items"""
        response = self.client.get(reverse('menu-list'))
        menus = Menu.objects.all()
        serializer = MenuItemSerializer(menus, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.booking_data = {
            'name': 'John Doe',
            'no_of_guests': 4,
            'bookingdate': timezone.now()
        }
        self.booking = Booking.objects.create(**self.booking_data)
    
    def test_get_all_bookings(self):
        """Test retrieving all bookings (requires authentication)"""
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_booking(self):
        """Test creating a new booking"""
        new_booking_data = {
            'name': 'Jane Doe',
            'no_of_guests': 2,
            'bookingdate': timezone.now().isoformat()
        }
        response = self.client.post(reverse('booking-list'), new_booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
    
    def test_retrieve_booking(self):
        """Test retrieving a specific booking"""
        response = self.client.get(reverse('booking-detail', args=[self.booking.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.booking_data['name'])

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.booking_data = {
            'name': 'John Doe',
            'no_of_guests': 4,
            'bookingdate': timezone.now().isoformat()
        }
    
    def test_unauthorized_request(self):
        """Test that unauthorized requests are rejected"""
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_authentication(self):
        """Test token authentication process"""
        # Get token
        response = self.client.post(reverse('api-token-auth'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
        # Use token for authenticated request
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
