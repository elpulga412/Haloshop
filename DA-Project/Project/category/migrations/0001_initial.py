# Generated by Django 4.0 on 2022-03-08 03:31

import category.models
import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Thương hiệu')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=category.models.upload_location)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
