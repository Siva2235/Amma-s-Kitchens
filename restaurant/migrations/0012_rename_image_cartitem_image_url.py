# Generated by Django 5.1.6 on 2025-03-10 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_cartitem_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='image',
            new_name='image_url',
        ),
    ]
