# Generated by Django 2.0.7 on 2018-08-02 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_sub_kind_enum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dinner_Platter_Kind_Enum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=32)),
            ],
        ),
    ]