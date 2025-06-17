from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AdForm, MultipleImageUploadForm
from .models import Ad, AdImage, SubCategory, Category
from django.core.exceptions import ObjectDoesNotExist

# views.py
from .models import Ad, AdImage, SubCategory, Category, Location

def post_ad(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = AdForm(request.POST)
        image_form = MultipleImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # ✅ Get location fields from POST
            country = request.POST.get('country')
            state = request.POST.get('state')
            city = request.POST.get('city')
            area = request.POST.get('area', '')

            if not all([country, state, city]):
                form.add_error(None, "Country, State, and City are required.")
                return render(request, 'sellForm.html', {
                    'form': form,
                    'image_form': image_form,
                    'categories': Category.objects.all()
                })

            # ✅ Create or get Location object
            location, _ = Location.objects.get_or_create(
                country=country.strip(),
                state=state.strip(),
                city=city.strip(),
                defaults={'area': area.strip()}
            )

            # ✅ Save the ad
            ad = form.save(commit=False)
            ad.user = request.user
            ad.location = location
            ad.save()

            # ✅ Handle image uploads
            images = request.FILES.getlist('images')
            error_messages = []

            if len(images) > 6:
                error_messages.append("You can upload a maximum of 6 images.")
            else:
                for img in images:
                    if img.size > 5 * 1024 * 1024:
                        error_messages.append(f"{img.name} is larger than 5MB.")
                        continue
                    if not img.content_type.startswith('image/'):
                        error_messages.append(f"{img.name} is not a valid image.")
                        continue
                    AdImage.objects.create(ad=ad, image=img)

            if error_messages:
                for msg in error_messages:
                    image_form.add_error('images', msg)
                return render(request, 'sellForm.html', {
                    'form': form,
                    'image_form': image_form,
                    'categories': Category.objects.all()
                })

            return redirect('ad_detail', slug=ad.slug, id=ad.id)  # ✅ Correct


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
