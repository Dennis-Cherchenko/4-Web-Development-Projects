# Generated by Django 2.0.7 on 2018-08-02 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20180802_0705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart_item',
            old_name='order_Id',
            new_name='order_id',
        ),
    ]
