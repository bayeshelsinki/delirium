# 0003_populate_token.py

from django.db import migrations
import uuid

def populate_tokens(apps, schema_editor):
    Profile = apps.get_model('crawl', 'Profile')
    for profile in Profile.objects.all():
        profile.token = uuid.uuid4()
        profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0002_profile_token'),
    ]

    operations = [
        migrations.RunPython(populate_tokens),
    ]
