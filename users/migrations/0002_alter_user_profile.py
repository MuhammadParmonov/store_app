# Generated by Django 4.2.7 on 2023-11-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(default='default_user.png', upload_to='profile_images/'),
        ),
    ]
