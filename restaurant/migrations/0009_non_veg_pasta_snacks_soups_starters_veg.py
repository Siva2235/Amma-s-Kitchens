# Generated by Django 5.1.6 on 2025-03-08 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_breakfast_data_category_alter_breakfast_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Non_Veg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_category', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='Non-Veg')),
                ('veg', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_category', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='pics')),
                ('veg', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Snacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_category', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='pics')),
                ('veg', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Soups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_category', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='pics')),
                ('veg', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Starters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_category', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='pics')),
                ('veg', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Veg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_category', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='Veg')),
                ('veg', models.BooleanField(default=True)),
            ],
        ),
    ]
