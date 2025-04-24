from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Show, ShowTime, Seat

class ShowListView(ListView):
    model = Show
    template_name = 'shows/show_list.html'
    context_object_name = 'shows'
    paginate_by = 6  # Show 6 shows per page
    
    def get_queryset(self):
        queryset = Show.objects.filter(is_active=True)
        
        # Filter by category if provided
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # The model's Meta class already orders by category (Indian first)
        return queryset

class ShowDetailView(DetailView):
    model = Show
    template_name = 'shows/show_detail.html'
    context_object_name = 'show'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get upcoming showtimes
        context['showtimes'] = self.object.showtimes.all()
        return context

class SeatSelectionView(LoginRequiredMixin, View):
    template_name = 'shows/seat_selection.html'
    
    def get(self, request, showtime_id):
        showtime = get_object_or_404(ShowTime, id=showtime_id)
        seats = Seat.objects.filter(showtime=showtime)
        
        # If seats don't exist yet, create them
        if not seats.exists():
            self._create_seats(showtime)
            seats = Seat.objects.filter(showtime=showtime)
        
        # Group seats by row for better display
        seat_map = {}
        for seat in seats:
            if seat.row not in seat_map:
                seat_map[seat.row] = []
            seat_map[seat.row].append(seat)
        
        # Sort rows
        sorted_seat_map = {row: seat_map[row] for row in sorted(seat_map.keys())}
        
        context = {
            'showtime': showtime,
            'seat_map': sorted_seat_map,
        }
        return render(request, self.template_name, context)
    
    def _create_seats(self, showtime):
        # Create a standard seating arrangement
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        seats_per_row = 10
        
        for row in rows:
            for num in range(1, seats_per_row + 1):
                Seat.objects.create(
                    showtime=showtime,
                    row=row,
                    number=num,
                    is_reserved=False
                )