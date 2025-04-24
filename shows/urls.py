from django.urls import path
from . import views

app_name = 'shows'

urlpatterns = [
    path('', views.ShowListView.as_view(), name='list'),
    path('<int:pk>/', views.ShowDetailView.as_view(), name='detail'),
    path('showtime/<int:showtime_id>/seats/', views.SeatSelectionView.as_view(), name='seat_selection'),
]