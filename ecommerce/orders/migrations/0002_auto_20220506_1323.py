# Generated by Django 3.2 on 2022-05-06 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderdetail',
            options={'verbose_name': 'OrderDetail', 'verbose_name_plural': 'OrderDetails'},
        ),
    ]
