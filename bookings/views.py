from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Booking, BookedSeat
from shows.models import ShowTime, Seat

class BookingHistoryView(LoginRequiredMixin, ListView):
    template_name = 'bookings/booking_history.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class CreateBookingView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, showtime_id):
        showtime = get_object_or_404(ShowTime, id=showtime_id)
        selected_seat_ids = request.POST.getlist('selected_seats')
        
        if not selected_seat_ids:
            messages.error(request, 'Please select at least one seat.')
            return redirect('shows:seat_selection', showtime_id=showtime.id)
        
        # Get selected seats and verify they are available
        selected_seats = Seat.objects.filter(id__in=selected_seat_ids, showtime=showtime)
        
        if selected_seats.filter(is_reserved=True).exists():
            messages.error(request, 'Some of the selected seats are already reserved. Please try again.')
            return redirect('shows:seat_selection', showtime_id=showtime.id)
        
        # Calculate total price
        total_price = showtime.price * len(selected_seats)
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            total_price=total_price
        )
        
        # Create booked seats and mark seats as reserved
        for seat in selected_seats:
            BookedSeat.objects.create(booking=booking, seat=seat)
            seat.is_reserved = True
            seat.save()
        
        messages.success(request, 'Booking successful!')
        return redirect('bookings:detail', pk=booking.id)