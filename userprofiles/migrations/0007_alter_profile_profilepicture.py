# Generated by Django 4.2.6 on 2024-10-01 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0006_profile_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profilepicture',
            field=models.ImageField(default='unknown-user.png', upload_to='images/'),
        ),
    ]
