# Generated by Django 2.0.7 on 2018-08-02 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20180802_0608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart_item',
            old_name='orderId',
            new_name='order_Id',
        ),
        migrations.RenameField(
            model_name='cart_item',
            old_name='userId',
            new_name='user_Id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='userId',
            new_name='user_Id',
        ),
    ]
