# Generated by Django 4.0.3 on 2022-06-11 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyKart', '0005_delete_customer_delete_product_alter_cart_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='totalamt',
            field=models.IntegerField(default=0),
        ),
    ]
