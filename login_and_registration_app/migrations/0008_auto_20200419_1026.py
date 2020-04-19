# Generated by Django 2.2 on 2020-04-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0007_auto_20200419_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='default_photo',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='profile_images'),
        ),
    ]