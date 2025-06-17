from django.shortcuts import render
from Sell.models import Category,Ad,Location
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
    location =Location.objects.all()[:7]
    
    return render(request, 'Home.html', {
        'categories': categories,
        'products': products,
        'location': location
    })


def ad_detail(request, slug, id):
    item = Ad.objects.filter(id=id).first()
    if not item:
        return render(request, '404.html', status=404)
    return render(request, 'ad_detail.html', {'item': item, 'slug': slug})

from django.db.models import Q

def search(request):
    query = request.GET.get('search-ad', '').strip()
    product_list = Ad.objects.filter(status='active')

    if query:
        # Split the query into words for broader matching
        words = query.split()

        # Build a dynamic Q object for partial matching
        q_object = Q(title__icontains=query)  # whole phrase match

        for word in words:
            q_object |= Q(title__icontains=word)
            q_object |= Q(category__name__icontains=word)
            q_object |= Q(subcategory__name__icontains=word)

        product_list = product_list.filter(q_object).distinct().order_by('-created_at').prefetch_related('images')
    else:
        product_list = Ad.objects.none()

    paginator = Paginator(product_list, 12)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'query': query
    })


def filter_category(request, id):
    category = Category.objects.filter(id=id).first()
    if not category:
        return render(request, '404.html', status=404)

    product_list = Ad.objects.filter(category=category, status='active') \
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

    return render(request, 'category_page.html', {
        'categories': categories,
        'products': products,
        'category': category
      
    })

from django.db.models import Q

def filter_by_location(request, slug=None):
    query = request.GET.get('q')
    
    if slug:
        # Slug-based navigation (e.g., from dropdown link)
        ads = Ad.objects.filter(
            Q(location__country__icontains=slug) |
            Q(location__state__icontains=slug) |
            Q(location__city__icontains=slug) |
            Q(location__area__icontains=slug),
            status='active'
        )
    elif query:
        # Search input
        ads = Ad.objects.filter(
            Q(location__country__icontains=query) |
            Q(location__state__icontains=query) |
            Q(location__city__icontains=query) |
            Q(location__area__icontains=query),
            status='active'
        )
    else:
        ads = Ad.objects.none()
        
    return render(request, 'Home.html', {'ads': ads})
