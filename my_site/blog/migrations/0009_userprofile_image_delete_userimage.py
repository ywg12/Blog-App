# Generated by Django 4.2.4 on 2023-08-21 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_userprofile_image_userimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
        migrations.DeleteModel(
            name='UserImage',
        ),
    ]
