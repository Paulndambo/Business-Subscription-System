# Generated by Django 5.1.4 on 2024-12-10 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0011_subscription_subscription_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="authorization_url",
            field=models.UUIDField(null=True),
        ),
    ]
