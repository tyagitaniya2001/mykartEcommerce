# Generated by Django 4.0.3 on 2022-07-08 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0009_sponsor_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='keywords',
        ),
        migrations.AddField(
            model_name='product',
            name='keywords',
            field=models.TextField(default=0),
        ),
    ]
