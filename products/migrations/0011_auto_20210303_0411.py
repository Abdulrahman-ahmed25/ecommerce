# Generated by Django 3.1.7 on 2021-03-03 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210303_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeatured',
            name='text_css_color',
            field=models.CharField(default='white', max_length=50),
        ),
    ]
