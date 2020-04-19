# Generated by Django 2.2 on 2020-04-19 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0003_user_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='photo',
            new_name='profile_photo',
        ),
        migrations.AddField(
            model_name='user',
            name='default_photo',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
