# Generated by Django 5.1.5 on 2025-01-26 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_remove_product_description1_remove_product_title1'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='email',
            field=models.EmailField(default=1, max_length=254, verbose_name='Почта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='message',
            field=models.TextField(default=1, verbose_name='Введите сообщение'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=1, max_length=255, verbose_name='Имя'),
            preserve_default=False,
        ),
    ]
