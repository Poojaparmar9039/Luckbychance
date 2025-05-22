from django.shortcuts import render
from Sell.models import Category,Ad
from django.shortcuts import render




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from Sell.models import Category, Ad, AdImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    # Get active products with their first image
    product_list = Ad.objects.filter(status='active') \
                   .order_by('-created_at') \
                   .prefetch_related('images')
    
    paginator = Paginator(product_list, 12)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    return render(request, 'Home.html', {
        'categories': categories,
        'products': products
    })


def ad_detail(request, slug):
    return render(request, 'ad_detail.html', {'slug': slug})
