# Generated by Django 4.2.5 on 2023-09-15 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="address",
            field=models.TextField(default=" "),
        ),
    ]