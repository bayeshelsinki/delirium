import os
import django

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delirium.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User
from crawl.models import Status, DrinkLog

def delete_non_superusers():
    # Fetch all non-superuser users
    non_superusers = User.objects.filter(is_superuser=False)

    # Get IDs of non-superuser users
    non_superuser_ids = non_superusers.values_list('id', flat=True)

    # Delete all Status entries related to non-superuser users
    status_count = Status.objects.filter(user_id__in=non_superuser_ids).count()
    Status.objects.filter(user_id__in=non_superuser_ids).delete()

    # Delete all DrinkLog entries related to non-superuser users
    drinklog_count = DrinkLog.objects.filter(user_id__in=non_superuser_ids).count()
    DrinkLog.objects.filter(user_id__in=non_superuser_ids).delete()

    # Delete all non-superuser users
    user_count = non_superusers.count()
    non_superusers.delete()

    print(f'Successfully deleted {user_count} non-superuser users.')
    print(f'Successfully deleted {status_count} Status entries.')
    print(f'Successfully deleted {drinklog_count} DrinkLog entries.')

if __name__ == '__main__':
    delete_non_superusers()
