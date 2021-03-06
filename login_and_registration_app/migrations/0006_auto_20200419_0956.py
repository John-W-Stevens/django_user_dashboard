# Generated by Django 2.2 on 2020-04-19 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0005_auto_20200419_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AlterField(
            model_name='user',
            name='default_photo',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
    ]
