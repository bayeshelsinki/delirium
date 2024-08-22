#!/usr/bin/env python
import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont
import qrcode
from django.conf import settings
from dotenv import load_dotenv

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delirium.settings')  # Adjust this to your settings module
django.setup()

from django.contrib.auth.models import User
from crawl.models import Profile  # Ensure this path is correct

def generate_qr_code_for_user(user):
    import qrcode  # Ensure qrcode library is installed: pip install qrcode[pil]
    from django.conf import settings

    # Ensure token exists
    token = user.profile.token
    site_url = 'https://www.delirium.fi'
    qr_data = f'{site_url}/login/{token}/'
    qr_img = qrcode.make(qr_data)

    # Set the dimensions of the final image
    width_cm = 8
    height_cm = 12
    dpi = 300  # DPI setting
    width_px = int(width_cm * dpi / 2.54)  # Convert cm to pixels
    height_px = int(height_cm * dpi / 2.54)

    # Create a new image with a white background
    final_img = Image.new('RGBA', (width_px, height_px), 'white')

    # Convert the QR code image to RGBA mode and resize
    qr_img = qr_img.convert('RGBA')
    qr_img = qr_img.resize((int(width_px * 0.8), int(height_px * 0.6)))  # Resize QR code

    # Paste the QR code into the final image
    final_img.paste(qr_img, (int(width_px * 0.1), int(height_px * 0.3)), qr_img)

    # Define magenta color
    magenta = (255, 8, 111, 255)

    # Draw the title text in magenta
    title_text = "Delirium 2024"
    try:
        title_font = ImageFont.truetype("Pacifico-Regular.ttf", 120)  # Adjust path and size
    except IOError:
        title_font = ImageFont.load_default()

    # Create an image for the text
    text_draw = ImageDraw.Draw(final_img)
    text_bbox = text_draw.textbbox((0, 0), title_text, font=title_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = 200
    
    text_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_img)

    # Draw text on the text image with magenta color
    draw_text.text((0, 0), title_text, font=title_font, fill=magenta)

    # Paste text onto the final image
    text_y_position = 100  # Adjust as needed
    final_img.paste(text_img, ((width_px - text_width) // 2, text_y_position), text_img)

    # Save the image
    qr_code_path = f'media/qr_codes/{user.username}_qr.png'
    os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
    final_img.save(qr_code_path)

    return qr_code_path

def create_user_and_qr(username, email):
    # Check if user already exists
    user, created = User.objects.get_or_create(username=username, email=email)

    if not created:
        print(f'User {username} already exists!')
    else:
        print(f'User {username} created successfully!')

    # Check if Profile already exists for the user
    profile, profile_created = Profile.objects.get_or_create(user=user)

    if profile_created:
        print(f'Profile created for user {username}!')
    else:
        print(f'Profile already exists for user {username}!')

    # Generate QR code
    qr_code_path = generate_qr_code_for_user(user)

    # Construct the URL for the QR code image with token
    token = user.profile.token
    qr_code_url = f'{settings.SITE_URL}/media/qr_codes/{user.username}_qr.png'

    print(f'QR code generated at: {qr_code_path}')
    print(f'QR code URL: {qr_code_url} (Token: {token})')

if __name__ == "__main__":
    for i in range(1, 51):  # Create users from user_01 to user_50
        username = f'user_{i:02}'  # Format number with leading zeros
        email = ''  # Empty email as required
        create_user_and_qr(username, email)
