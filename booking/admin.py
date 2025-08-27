from django.contrib import admin
from .models import Airline, Airport, Flight, Booking, Passenger, Ticket, Payment

# Register your models here.

admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Payment)
