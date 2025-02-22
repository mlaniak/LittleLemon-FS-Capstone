from django.test import TestCase
from restaurant.models import Menu, Category, Booking
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from datetime import date

class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Main Course",
            order=1
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, "Main Course")
        self.assertEqual(self.category.order, 1)
    
    def test_category_str(self):
        self.assertEqual(str(self.category), "Main Course")

class MenuTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Desserts",
            order=2
        )
        self.menu_item = Menu.objects.create(
            title="Tiramisu",
            price=Decimal('8.99'),
            inventory=20,
            description="Classic Italian dessert",
            category=self.category
        )
    
    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.title, "Tiramisu")
        self.assertEqual(self.menu_item.price, Decimal('8.99'))
        self.assertEqual(self.menu_item.inventory, 20)
        self.assertEqual(self.menu_item.description, "Classic Italian dessert")
        self.assertEqual(self.menu_item.category, self.category)
    
    def test_menu_string_representation(self):
        self.assertEqual(str(self.menu_item), "Tiramisu : 8.99")

class BookingTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="John",
            reservation_date=date(2024, 3, 15),
            reservation_slot="18:00"
        )
    
    def test_booking_creation(self):
        self.assertEqual(self.booking.first_name, "John")
        self.assertEqual(self.booking.reservation_date, date(2024, 3, 15))
        self.assertEqual(self.booking.reservation_slot, "18:00")
    
    def test_empty_name_validation(self):
        with self.assertRaises(ValidationError):
            booking = Booking(
                first_name="",
                reservation_date=date(2024, 3, 15),
                reservation_slot="18:00"
            )
            booking.full_clean()
    
    def test_unique_reservation_slot(self):
        with self.assertRaises(ValidationError):
            # Try to create a booking for the same date and slot
            Booking.objects.create(
                first_name="Jane",
                reservation_date=date(2024, 3, 15),
                reservation_slot="18:00"
            )
