# Generated by Django 5.0.4 on 2024-06-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Index", "0006_rename_order_orderitem_orders"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orders",
            name="total",
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
