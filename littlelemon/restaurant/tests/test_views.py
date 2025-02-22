from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from restaurant.models import Menu, Category, Booking
from restaurant.serializers import MenuItemSerializer, CategorySerializer, BookingSerializer
from decimal import Decimal
from datetime import date
from rest_framework.authtoken.models import Token

class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.category1 = Category.objects.create(name="Main Course", order=1)
        self.category2 = Category.objects.create(name="Desserts", order=2)
    
    def test_get_categories(self):
        """Test retrieving all categories"""
        response = self.client.get(reverse('category-list'))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_category(self):
        """Test creating a new category"""
        data = {'name': 'Beverages', 'order': 3}
        response = self.client.post(reverse('category-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name='Beverages').exists())

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.category = Category.objects.create(name="Main Course", order=1)
        self.menu1 = Menu.objects.create(
            title="Pizza Margherita",
            price=Decimal('12.99'),
            inventory=50,
            description="Classic Italian pizza",
            category=self.category
        )
        self.menu2 = Menu.objects.create(
            title="Pasta Carbonara",
            price=Decimal('10.99'),
            inventory=30,
            description="Creamy pasta dish",
            category=self.category
        )
    
    def test_get_menu_items(self):
        """Test retrieving all menu items"""
        response = self.client.get(reverse('menu-list'))
        menus = Menu.objects.all()
        serializer = MenuItemSerializer(menus, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_menu_item(self):
        """Test creating a new menu item"""
        data = {
            'title': 'Lasagna',
            'price': '13.99',
            'inventory': 25,
            'description': 'Layered pasta dish',
            'category_id': self.category.id
        }
        response = self.client.post(reverse('menu-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Menu.objects.filter(title='Lasagna').exists())

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
            'first_name': 'John',
            'reservation_date': date(2024, 3, 15),
            'reservation_slot': '18:00'
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
            'first_name': 'Jane',
            'reservation_date': '2024-03-16',
            'reservation_slot': '19:00'
        }
        response = self.client.post(reverse('booking-list'), new_booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
    
    def test_duplicate_booking_slot(self):
        """Test that duplicate booking slots are rejected"""
        duplicate_booking = {
            'first_name': 'Jane',
            'reservation_date': '2024-03-15',
            'reservation_slot': '18:00'
        }
        response = self.client.post(reverse('booking-list'), duplicate_booking, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com',
            're_password': 'testpass123'  # Djoser requires password confirmation
        }
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post('/auth/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_user_login(self):
        """Test user login and token generation"""
        # Create user first
        User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            email=self.user_data['email']
        )
        
        # Try to login
        response = self.client.post('/auth/token/login/', {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)
    
    def test_unauthorized_access(self):
        """Test that unauthorized requests are rejected"""
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
