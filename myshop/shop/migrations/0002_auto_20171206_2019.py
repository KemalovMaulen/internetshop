# Generated by Django 2.0 on 2017-12-06 14:19

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=shop.models.upload_to_s3, verbose_name='Изображение товара'),
        ),
    ]
