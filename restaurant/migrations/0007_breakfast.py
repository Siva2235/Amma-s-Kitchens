# Generated by Django 5.1.6 on 2025-03-08 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_chef_combo_offers_quick_bites_refreshing_drinks'),
    ]

    operations = [
        migrations.CreateModel(
            name='BreakFast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='menu_images/breakfast/')),
                ('veg', models.BooleanField(default=True)),
            ],
        ),
    ]
