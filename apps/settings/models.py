from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from apps.utils import get_product_upload_path
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from slugify import slugify
import uuid
from django.urls import reverse
# Create your models here.



class Category(MPTTModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.TextField(verbose_name='Название')
    slug = models.CharField(max_length=255, verbose_name='SLUG', unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение категории', null=True, blank=True)
    parent = TreeForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Родительская категория', related_name='children'
    )
    is_active = models.BooleanField(verbose_name='Активная категория', default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.title)
            self.slug = original_slug
            num = 1
            # Ensure unique slug by appending a number if necessary
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{num}"
                num += 1
        super(Category, self).save(*args, **kwargs)
        
    def get_tree_display(self, key, delimiter):
        parent = self.parent.get_tree_display(key, delimiter) if self.parent else ''
        return f'{parent}{delimiter}{getattr(self, key)}' if parent else getattr(self, key)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def get_children(self):
        return Category.objects.filter(parent=self, is_active=True)

    def get_products_count(self):
        # Подсчет активных товаров в текущей и всех дочерних категориях
        descendants = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendants, is_active=True).count()

    def get_all_children(self):
        # Этот метод заменяется `get_descendants()` в MPTT
        return self.get_descendants(include_self=True)

    def get_all_parents(self):
        # Этот метод заменяется `get_ancestors()` в MPTT
        return self.get_ancestors(include_self=True)

    # def clean(self):
    #     # Предотвращение циклических ссылок
    #     if self.parent and self.parent in self.get_descendants():
    #         raise ValidationError("Категория не может быть родительской для самой себя или для своих потомков.")

    # def clean(self):  
    #     if self.parent in self.get_all_children():
    #         raise ValidationError("A user cannot have itself \
    #                    or one of its' children as parent.")


class Product(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Тут нужно писать название товара"
    )
    slug = models.TextField(
        verbose_name="SLUG",
        unique=True
        )
    
    category = TreeForeignKey(
        to = "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )


    title1 = models.CharField(
        max_length=255,
        verbose_name="Прозвище",
        help_text="Тут нужно писать прозвище товара"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Тут нужно писать описание товара"
    )
    description1 = models.TextField(
        verbose_name="Описание",
        help_text="Тут нужно писать описание того как этот товар готовили"
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            while Product.pobjects.filter(slug=self.slug).exists():
               unique_suffix = uuid.uuid4().hex[:6]
               self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

    
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
