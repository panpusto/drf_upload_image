# Generated by Django 4.1.7 on 2023-03-04 21:22

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='link',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=images.models.path_to_upload_img),
        ),
    ]