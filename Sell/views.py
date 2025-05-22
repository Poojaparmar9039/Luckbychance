from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AdForm, MultipleImageUploadForm
from .models import Ad, AdImage, SubCategory, Category
from django.core.exceptions import ObjectDoesNotExist

# views.py
def post_ad(request):
    if not request.user.is_authenticated:  # Better way to check authentication
        return redirect('login')

    if request.method == 'POST':
        form = AdForm(request.POST)
        image_form = MultipleImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # First save the ad without images
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()

            # Then handle images if form is valid
            images = request.FILES.getlist('images')
            error_messages = []

            if len(images) > 6:
                error_messages.append("You can upload a maximum of 6 images.")
            else:
                for img in images:
                    if img.size > 5 * 1024 * 1024:  # 5MB
                        error_messages.append(f"{img.name} is larger than 5MB.")
                        continue
                    if not img.content_type.startswith('image/'):
                        error_messages.append(f"{img.name} is not a valid image.")
                        continue
                    AdImage.objects.create(ad=ad, image=img)

            if error_messages:
                # If there are image errors, show them with the form
                for msg in error_messages:
                    image_form.add_error('images', msg)
                return render(request, 'sellForm.html', {
                    'form': form,
                    'image_form': image_form,
                    'categories': Category.objects.all()
                })

            return redirect('ad_detail', slug=ad.slug)
        else:
            # Form is invalid, show errors
            return render(request, 'sellForm.html', {
                'form': form,
                'image_form': image_form,
                'categories': Category.objects.all()
            })

    else:
        form = AdForm()
        image_form = MultipleImageUploadForm()

    return render(request, 'sellForm.html', {
        'form': form,
        'image_form': image_form,
        'categories': Category.objects.all()
    })

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
