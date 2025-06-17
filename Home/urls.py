from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('ad-detail/<slug:slug>/<uuid:id>/', views.ad_detail, name='ad_detail'),
    path('search/', views.search, name='search'),
    path('category/<int:id>/', views.filter_category, name='filter_category'),
    path('location/<slug:slug>/', views.filter_by_location, name='filter_by_location'),
    path('location/', views.filter_by_location, name='filter_by_location'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
