import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='Sell/category_icons/', blank=True, null=True)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class Location(models.Model):
    country = models.CharField(max_length=100,default='India')
    state = models.CharField(max_length=100,default='Indore')
    city = models.CharField(max_length=100,default='Indore')

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"


class Ad(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=False)
    condition = models.CharField(max_length=50, choices=[('new', 'New'), ('used', 'Used')])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Ad.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ad_images/')

    def __str__(self):
        return f"Image for {self.ad.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AdTag(models.Model):
    ad = models.ForeignKey(Ad, related_name='tags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ad', 'tag')

    def __str__(self):
        return f"{self.ad.title} → {self.tag.name}"
