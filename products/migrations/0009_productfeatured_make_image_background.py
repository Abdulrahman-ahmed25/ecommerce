# Generated by Django 3.1.7 on 2021-03-03 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productfeatured'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeatured',
            name='make_image_background',
            field=models.BooleanField(default=False),
        ),
    ]