# Generated by Django 5.1.4 on 2024-12-09 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("businesses", "0004_alter_business_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="business",
            name="description",
            field=models.TextField(null=True),
        ),
    ]