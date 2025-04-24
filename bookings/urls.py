from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('history/', views.BookingHistoryView.as_view(), name='history'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('create/<int:showtime_id>/', views.CreateBookingView.as_view(),  name='detail'),
    path('create/<int:showtime_id>/', views.CreateBookingView.as_view(), name='create'),
]