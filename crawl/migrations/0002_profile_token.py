# Generated by Django 5.1 on 2024-08-15 12:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crawl", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="token",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
