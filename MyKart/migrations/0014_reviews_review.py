# Generated by Django 4.0.3 on 2022-07-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyKart', '0013_reviews_alter_orders_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='review',
            field=models.TextField(default=''),
        ),
    ]
