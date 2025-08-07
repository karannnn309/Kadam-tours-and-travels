# bookings/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Booking

@receiver(post_save, sender=Booking)
def send_confirmation_email(sender, instance, created, **kwargs):
    # Only send email when status changes to confirmed, not on creation
    if not created:
        if instance.status == 'confirmed':
            # You can also check if the status actually changed here if needed (requires a custom check or middleware)
            subject = 'Your Booking is Confirmed'
            message = (
                f"Dear {instance.name},\n\n"
                f"Your booking for {instance.vehicle.name} on {instance.datetime.strftime('%Y-%m-%d %H:%M')} "
                f"from {instance.pickup_location} to {instance.drop_location} has been confirmed.\n\n"
                "Thank you for choosing Kadam Tours and Travels!"
            )
            send_mail(
                subject,
                message,
                'rananawarekaran214@gmail.com',  # From email (admin/owner)
                [instance.email],  # To customer
                fail_silently=False
            )
