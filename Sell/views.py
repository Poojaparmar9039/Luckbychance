from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AdForm, MultipleImageUploadForm
from .models import Ad, AdImage, SubCategory, Category


def post_ad(request):
    if not request.session.get('user_id'):
        return redirect('login')
    if request.method == 'POST':
        form = AdForm(request.POST)
        image_form = MultipleImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid() and image_form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            
   
            images = request.FILES.getlist('images') if hasattr(request.FILES, 'getlist') else [request.FILES.get('images')]
            for img in images[:6]: 
                if img: 
                    AdImage.objects.create(ad=ad, image=img)
            
            return redirect('ad_detail', slug=ad.slug)
    else:
        form = AdForm()
        image_form = MultipleImageUploadForm()

    categories = Category.objects.all()
    return render(request, 'sellForm.html', {
        'form': form,
        'image_form': image_form,
        'categories': categories
    })

from django.core.exceptions import ObjectDoesNotExist

def load_subcategories(request):
    try:
        category_id = request.GET.get('category_id')
        if not category_id:
            return JsonResponse([], safe=False)
        subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
        
    except ObjectDoesNotExist:
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)