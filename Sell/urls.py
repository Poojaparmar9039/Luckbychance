from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post-ad/', views.post_ad, name='post_ad'),
    path('load-subcategories/', views.load_subcategories, name='load_subcategories'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)