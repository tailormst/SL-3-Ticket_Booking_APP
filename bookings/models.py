from django.db import models
from django.contrib.auth.models import User
from shows.models import ShowTime, Seat

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"
    
    class Meta:
        ordering = ['-booking_date']

class BookedSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_seats')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.seat} - Booking #{self.booking.id}"
    
    class Meta:
        unique_together = ('booking', 'seat')