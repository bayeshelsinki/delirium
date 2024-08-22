from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
import qrcode
import os

class Command(BaseCommand):
    help = 'Generate QR codes for all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if hasattr(user, 'profile'):
                self.generate_qr_code_for_user(user)

    def generate_qr_code_for_user(self, user):
        qr_data = f'{settings.SITE_URL}/login/{user.profile.token}/'
        img = qrcode.make(qr_data)
        qr_code_path = f'media/qr_codes/{user.username}_qr.png'
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
        img.save(qr_code_path)
        self.stdout.write(self.style.SUCCESS(f'Generated QR code for {user.username}'))
