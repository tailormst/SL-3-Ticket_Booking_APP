from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # App URLs
    path('users/', include('users.urls')),
    path('shows/', include('shows.urls')),
    path('bookings/', include('bookings.urls')),
    path('admin-panel/', include('admin_panel.urls')),  # Custom admin panel
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)