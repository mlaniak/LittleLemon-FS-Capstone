from django.core.management.base import BaseCommand
from restaurant.models import Booking
from django.db.models import Count

class Command(BaseCommand):
    help = 'Removes duplicate bookings keeping only the first entry'

    def handle(self, *args, **options):
        # Find duplicates
        duplicates = (
            Booking.objects.values('reservation_date', 'reservation_slot')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        removed_count = 0
        for dup in duplicates:
            # Get all bookings for this date and slot
            bookings = Booking.objects.filter(
                reservation_date=dup['reservation_date'],
                reservation_slot=dup['reservation_slot']
            ).order_by('id')
            
            # Keep the first one, delete the rest
            first_booking = bookings.first()
            bookings.exclude(id=first_booking.id).delete()
            removed_count += bookings.count() - 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully removed {removed_count} duplicate bookings')
        )
