# Generated by Django 4.2.2 on 2023-06-08 21:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0010_rename_merchant_id_order_payment_intent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment_intent",
            field=models.CharField(max_length=3000),
        ),
    ]
