# Generated by Django 3.2 on 2022-04-22 06:34

from django.db import migrations, models
import ecommerce.utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationuser',
            name='height_photo',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationuser',
            name='photo',
            field=models.ImageField(blank=True, height_field='height_photo', null=True, upload_to=ecommerce.utils.utils.get_user_photo_random_filename, width_field='width_photo'),
        ),
        migrations.AddField(
            model_name='applicationuser',
            name='width_photo',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
