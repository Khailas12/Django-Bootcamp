# Generated by Django 3.2.7 on 2021-10-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_product_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='can_backorder',
            field=models.BooleanField(default=False),
        ),
    ]