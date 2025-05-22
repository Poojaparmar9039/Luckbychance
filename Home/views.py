from django.shortcuts import render
from .models import Country
from Sell.models import Category

def home(request):
    countries = Country.objects.all()
    categories = Category.objects.all()
    return render(request, 'Home.html', {'countries': countries,'categories': categories})




def ad_deatil(request):
    return render(request, 'ad_detail.html')