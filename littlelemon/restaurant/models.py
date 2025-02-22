from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    
    def get_item(self):
        return f'{self.title} : {str(self.price)}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)  # For controlling display order

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    description = models.TextField(default='', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='menu_items')

    def __str__(self):
        return f'{self.title} : {self.price}'

    class Meta:
        verbose_name_plural = "Menu Items"
        ordering = ['category__order', 'title']

class Booking(models.Model):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    reservation_date = models.DateField()
    reservation_slot = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['reservation_date', 'reservation_slot']
        ordering = ['reservation_date', 'reservation_slot']

    def clean(self):
        if not self.first_name or not self.first_name.strip():
            raise ValidationError('Name cannot be empty')

    def save(self, *args, **kwargs):
        self.full_clean()
        self.first_name = self.first_name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} at {self.reservation_slot}"
