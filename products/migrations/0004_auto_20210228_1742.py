# Generated by Django 3.1.7 on 2021-02-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210220_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='variation',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]