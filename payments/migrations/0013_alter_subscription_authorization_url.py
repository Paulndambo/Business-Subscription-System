# Generated by Django 5.1.4 on 2024-12-10 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0012_subscription_authorization_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="authorization_url",
            field=models.URLField(null=True),
        ),
    ]
