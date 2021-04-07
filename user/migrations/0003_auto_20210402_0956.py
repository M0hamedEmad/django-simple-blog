# Generated by Django 3.1.7 on 2021-04-02 07:56

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210401_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='user/default.jpg', null=True, upload_to=user.models.upload_image),
        ),
    ]
