# Generated by Django 4.2.2 on 2023-06-08 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userprofiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="is_vendor",
            field=models.BooleanField(default=False),
        ),
    ]
