from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import Vehicle, Booking
from .forms import BookingForm, ContactForm
from django.contrib import messages

def home(request):
    vehicles = Vehicle.objects.filter(is_active=True)
    booking_form = BookingForm()
    contact_form = ContactForm()
    return render(request, 'core/home.html', {
        'vehicles': vehicles,
        'booking_form': booking_form,
        'contact_form': contact_form,
        'admin_email': settings.ADMIN_EMAIL,
    })

def book_ride(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = 'pending'  # Admin will confirm later
            booking.save()

            admin_url = request.build_absolute_uri(
                reverse('admin:core_booking_change', args=[booking.id])
            )

            # Optional: notify admin that a new booking was requested
            admin_subject = f"[New Booking - Pending] {booking.name} | {booking.vehicle.name}"
            admin_msg = (
                f"A new booking has been requested:\n\n"
                f"Name: {booking.name}\n"
                f"Vehicle: {booking.vehicle.name}\n"
                f"Pickup: {booking.pickup_location}\n"
                f"Drop: {booking.drop_location}\n"
                f"Date & Time: {booking.datetime.strftime('%Y-%m-%d %H:%M')}\n"
                f"Email: {booking.email}\n"
                f"Phone: {booking.phone}\n"
                f"Status: Pending\n\n"
                f"Review and confirm here:\n{admin_url}"
            )
            send_mail(f"New Booking Request: {booking.name}",admin_subject, admin_msg, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

            messages.success(request, "Booking request submitted. We'll confirm shortly.")
            return redirect(reverse('core:home'))
        else:
            messages.error(request, "There was a problem with your booking. Please correct the errors.")
    return redirect('core:home')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            send_mail(
                f"[Contact] {data['subject']}",
                f"From: {data['name']} <{data['email']}>\n\n{data['message']}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
            )
            messages.success(request, "Message sent. We'll get back to you soon.")
            return redirect(reverse('core:home'))
        else:
            messages.error(request, "Please fix the errors in the contact form.")
    return redirect('core:home')

