from django.urls import path
from . import views

urlpatterns = [
     path('sign/', views.sign, name='sign'),
    path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]
