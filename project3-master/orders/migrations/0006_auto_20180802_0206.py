# Generated by Django 2.0.7 on 2018-08-02 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20180801_2353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dinner_platter',
            old_name='price',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='pasta',
            old_name='price',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='pizza',
            old_name='price',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='pizza_topping',
            old_name='price',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='salad',
            old_name='price',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='sub',
            old_name='price',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='sub_topping',
            old_name='price',
            new_name='cost',
        ),
    ]
