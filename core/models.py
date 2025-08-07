from django.db import models
from django.utils import timezone

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(help_text="Max passengers")
    fare_per_km = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='vehicles/')
    is_active = models.BooleanField(default=True)  # show/hide
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def seats_available(self, booking_datetime):
        # naive implementation: count bookings at same datetime
        bookings = Booking.objects.filter(
            vehicle=self,
            datetime=booking_datetime,
            status='confirmed'
        )
        total_booked = sum(b.passengers for b in bookings)
        return max(self.capacity - total_booked, 0)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    passengers = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.vehicle.name} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"

