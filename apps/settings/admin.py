from django.contrib import admin
from apps.settings.models import Product, ProductImage
from django.utils.html import format_html

# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_tag']
    
    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="50px" />'.format(obj.image.url))
    
    image_tag.short_description = "Изображение"
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('title', 'description', 'price', 'is_active')
    list_editable=['is_active']
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': (
            'title',
            'description',
            'price',
            'is_active',
            'created_at',
        )}),
    )
    
    inlines = [ProductImageAdmin]
    
    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="30px" />'.format(obj.get_first_image()))

    image_tag.short_description = 'Изображение'
