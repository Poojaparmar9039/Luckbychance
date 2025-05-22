from django import forms
from .models import Ad, Category, SubCategory

class AdForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Ad
        fields = [
            'title', 'description', 'price', 'is_negotiable',
            'condition', 'category', 'subcategory', 'location',
            'contact_phone', 'contact_email', 'whatsapp_number',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'is_negotiable': forms.CheckboxInput(),
        }

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
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.subcategory.category)

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
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
        ]
    )
    
    def clean_images(self):
        images = self.files.getlist('images') if hasattr(self.files, 'getlist') else [self.files.get('images')]
        
        if not images or images[0] is None:
            if self.required:
                raise forms.ValidationError("Please upload at least one image")
            return []
            
        if len(images) > 6:
            raise forms.ValidationError("You can upload a maximum of 6 images.")
        
        for img in images:
            if img.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError(f"Image {img.name} is too large (max 5MB each)")
            if not img.content_type.startswith('image/'):
                raise forms.ValidationError(f"File {img.name} is not an image")
        
        return images