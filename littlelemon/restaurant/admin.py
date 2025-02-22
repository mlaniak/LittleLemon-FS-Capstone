from django.contrib import admin
from .models import Menu, Category, Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    ordering = ['order']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory', 'category']
    list_filter = ['category']
    search_fields = ['title', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'reservation_date', 'reservation_slot']
    list_filter = ['reservation_date']
    search_fields = ['first_name']
    date_hierarchy = 'reservation_date'
