# Generated by Django 3.1.7 on 2021-03-12 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
    ]
