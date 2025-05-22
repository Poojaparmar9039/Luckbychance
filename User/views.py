from django.shortcuts import render, redirect
from .models import User_Account
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import re
import random
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import datetime, timedelta


def validate_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Password strength validation"""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one number")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter")

def sign(request):
    if request.method == 'POST':
        try:
            fullname = request.POST.get('fullname', '').strip()
            email = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password', '').strip()

            if not all([fullname, email, password]):
                return render(request, 'sign.html', {'error': 'All fields are required'})
            if not validate_email(email):
                return render(request, 'sign.html', {'error': 'Please enter a valid email address'})
            try:
                validate_password(password)
            except ValidationError as e:
                return render(request, 'sign.html', {'error': str(e)})
            if User_Account.objects.filter(email=email).exists():
                return render(request, 'sign.html', {'error': 'Email already exists'})
            
            hashed_password = make_password(password)
            user = User_Account.objects.create(
                fullname=fullname,
                email=email,
                password=hashed_password
            )
            return render(request, 'login.html', {'message': 'Registration successful! Please log in'})
        except IntegrityError:
            return render(request, 'sign.html', {'error': 'Database error during registration'})
        except Exception as e:
            return render(request, 'sign.html', {'error': f'Unexpected error: {str(e)}'})
    return render(request, 'sign.html')

def login(request):
    # if request.session.get('user_id'):
    #     return redirect('home')  # Redirect to home if already logged in
    if request.method == 'POST':
        try:
            email = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password', '').strip()
            
            if not all([email, password]):
                return render(request, 'login.html', {'error': 'Both fields are required'})
            try:
                user = User_Account.objects.get(email=email)
            except User_Account.DoesNotExist:
                return render(request, 'login.html', {'error': 'Invalid email or password'})
            
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password'})
        except Exception as e:
            return render(request, 'login.html', {'error': f'Unexpected error: {str(e)}'})
    return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if not email:
            return render(request, 'forgot_password.html', {'error': 'Email is required'})
        try:
            user = User_Account.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)
            request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
            request.session['otp_verified'] = False

            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is {otp}. It is valid for 10 minutes.',
                EMAIL_HOST_USER,
                [email],
            )
            return render(request, 'verify_otp.html', {'message': 'OTP sent to your email. Please verify.'})
        except User_Account.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email not found'})
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp', '').strip()
        session_otp = request.session.get('reset_otp')
        expiry_str = request.session.get('otp_expiry')
        
        if not otp_input:
            return render(request, 'verify_otp.html', {'error': 'OTP is required'})
        if not session_otp or not expiry_str:
            return render(request, 'forgot_password.html', {'error': 'OTP session expired'})
        
        expiry = datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
        if datetime.now() > expiry:
            return render(request, 'forgot_password.html', {'error': 'OTP has expired'})
        if otp_input != session_otp:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
        
        request.session['otp_verified'] = True
        return render(request, 'reset_password.html', {'message': 'OTP verified successfully. You can now reset your password.'})
    return render(request, 'verify_otp.html')

def reset_password(request):
    if not request.session.get('otp_verified'):
        return render(request, 'forgot_password.html', {'error': 'Please verify OTP first'})

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not all([new_password, confirm_password]):
            return render(request, 'reset_password.html', {'error': 'All fields are required'})
        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match'})
        try:
            validate_password(new_password)
        except ValidationError as e:
            return render(request, 'reset_password.html', {'error': str(e)})

        email = request.session.get('reset_email')
        if not email:
            return render(request, 'forgot_password.html', {'error': 'Session expired'})

        user = User_Account.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        # Clean up session
        for key in ['reset_email', 'reset_otp', 'otp_expiry', 'otp_verified']:
            request.session.pop(key, None)

        return render(request, 'login.html', {'message': 'Password has been reset successfully.'})
    return render(request, 'reset_password.html')



def user_dashboard(request):
  
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User_Account.objects.get(id=user_id)
        return render(request, 'user_dashboard.html', {'user': user})
    except User_Account.DoesNotExist:
        return redirect('login')
    except Exception as e:
        return render(request, 'user_dashboard.html', {'error': f'Unexpected error: {str(e)}'})