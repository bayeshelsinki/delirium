# Generated by Django 5.1 on 2024-08-15 12:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crawl", "0003_populate_tokens"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
