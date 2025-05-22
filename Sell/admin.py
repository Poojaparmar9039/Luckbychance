from django.contrib import admin
from .models import  Category, SubCategory,Location, Ad, AdImage, Tag,AdTag

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Ad)
admin.site.register(AdImage)
admin.site.register(Tag)
admin.site.register(AdTag)
admin.site.register(Location)
