from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('ad-detail/', views.ad_deatil, name='ad_detail'),

    # path('get-states/', views.get_states, name='get_states'),
    # path('get-cities/', views.get_cities, name='get_cities'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
