from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from apps.utils import get_product_upload_path
# Create your models here.

class Product(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Тут нужно писать название товара"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Тут нужно писать описание товара"
    )
    price = models.DecimalField(
        max_digits=100, 
        decimal_places=2,
        verbose_name="Цена",
        help_text="Тут нужно писать цену товара"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        null=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя'
    )
    email = models.EmailField(
        verbose_name='Почта'
    )
    message = models.TextField(
        verbose_name="Введите сообщение"
    )

    def __str__(self):
        return self.title
    
    def get_first_image(self) -> 'ProductImage':
        product_image = ProductImage.objects.filter(product=self).first()
        return product_image.image.url if product_image else None
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        

        
class ProductImage(models.Model):
    product = models.ForeignKey(
        to='Product',
        on_delete=models.CASCADE,
        verbose_name="Изображение",
        related_name='product_image'
    )
    image = ProcessedImageField(
        upload_to=get_product_upload_path,
        verbose_name="Изображение",
        processors=[ResizeToFill(100, 50)],
        format='webp',
        options={'quality': 100},
        help_text="Ваше фото будет пересохранено на формат <webp>"
    )
    position = models.PositiveIntegerField(
        default=0,
        blank=True, null=True
    )
    
    def __str__(self):
        return str(self.image.name)

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'
        ordering = ['position', ]