# Generated by Django 3.2 on 2021-04-06 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagine', '0005_alter_gallery_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='images',
        ),
        migrations.AddField(
            model_name='gallery',
            name='images',
            field=models.ManyToManyField(blank=True, to='imagine.Image'),
        ),
    ]
