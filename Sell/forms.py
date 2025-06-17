from django import forms
from .models import Ad, Category, SubCategory

from django import forms
from .models import Ad, Category, SubCategory
from .models import Location  # make sure Location model is imported

# forms.py
class AdForm(forms.ModelForm):
    country = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    area = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Ad
        fields = [
            'title', 'description', 'price', 'is_negotiable',
            'condition', 'category', 'subcategory','seller_name',
            'contact_phone', 'contact_email', 'whatsapp_number',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'is_negotiable': forms.CheckboxInput(),
        }


    # Rest of the form remains the same...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.subcategory:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(
                category=self.instance.subcategory.category
            )


from .widgets import MultipleFileInput
from django.core.validators import FileExtensionValidator

class MultipleImageUploadForm(forms.Form):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'accept': 'image/*',
            'class': 'file-upload'
        }),
        required=False,
        label="Upload up to 6 images",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )








