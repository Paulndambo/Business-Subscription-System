# Generated by Django 5.1.4 on 2024-12-09 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_subscriptionpayment_subscription"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscriptionpayment",
            name="subscription",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="payments.subscription"
            ),
        ),
    ]
