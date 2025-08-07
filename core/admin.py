from django.contrib import admin
from .models import Vehicle, Booking
admin.site.site_header = "Kadam Tours and Travels Admin"
admin.site.site_title = "KTT Admin Portal"
admin.site.index_title = "Welcome to Kadam Tours and Travels Admin Panel"

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'fare_per_km', 'is_active')
    search_fields = ('name',)



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle', 'datetime', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'pickup_location', 'drop_location')
    list_editable = ('status',)  # Make status editable directly


