# Generated by Django 4.0.1 on 2022-02-16 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0004_rename_adress_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.IntegerField(default=1),
        ),
    ]
