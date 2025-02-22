from django.test import TestCase
from restaurant.models import Menu, MenuItem, Booking
from django.utils import timezone
from decimal import Decimal

class MenuTest(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            title="Pizza",
            price=Decimal('12.99'),
            inventory=50
        )
    
    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.title, "Pizza")
        self.assertEqual(self.menu_item.price, Decimal('12.99'))
        self.assertEqual(self.menu_item.inventory, 50)
    
    def test_menu_string_representation(self):
        self.assertEqual(str(self.menu_item), "Pizza - $12.99")

class MenuItemTest(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            title="IceCream",
            price=Decimal('80.00'),
            inventory=100
        )
    
    def test_get_item(self):
        self.assertEqual(self.menu_item.get_item(), "IceCream : 80.00")
    
    def test_menu_item_fields(self):
        self.assertEqual(self.menu_item.title, "IceCream")
        self.assertEqual(self.menu_item.price, Decimal('80.00'))
        self.assertEqual(self.menu_item.inventory, 100)

class BookingTest(TestCase):
    def setUp(self):
        self.booking_time = timezone.now()
        self.booking = Booking.objects.create(
            name="John Doe",
            no_of_guests=4,
            bookingdate=self.booking_time
        )
    
    def test_booking_creation(self):
        self.assertEqual(self.booking.name, "John Doe")
        self.assertEqual(self.booking.no_of_guests, 4)
        self.assertEqual(self.booking.bookingdate, self.booking_time)
    
    def test_booking_string_representation(self):
        expected_str = f"John Doe - {self.booking_time}"
        self.assertEqual(str(self.booking), expected_str)
