# Generated by Django 2.2 on 2021-08-26 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default='Book Description'),
        ),
    ]
