# Generated by Django 4.2 on 2023-05-04 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_category_options_alter_tours_photo_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tours',
            name='photo',
            field=models.ImageField(upload_to='static/img/gallery', verbose_name='Фотография'),
        ),
    ]