# import qrcode
# from django.conf import settings
# import os

# def generate_qr_code_for_user(user):
#     qr_data = f'{settings.SITE_URL}/login/{user.profile.token}/'
#     img = qrcode.make(qr_data)
#     qr_code_path = f'media/qr_codes/{user.username}_qr.png'
#     os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
#     img.save(qr_code_path)
#     return qr_code_path

import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from django.conf import settings

def generate_qr_code_for_user(user):
    # QR code data
    qr_data = f'{settings.SITE_URL}/login/{user.profile.token}/'
    
    # Generate QR code
    qr_img = qrcode.make(qr_data)
    
    # Create a new image with white background
    width_cm, height_cm = 12, 8  # Desired dimensions in cm
    dpi = 300  # Recommended DPI for print quality
    width_px = int(width_cm * dpi / 2.54)  # Convert cm to pixels
    height_px = int(height_cm * dpi / 2.54)  # Convert cm to pixels
    
    # Create a new image with white background
    new_img = Image.new('RGB', (width_px, height_px), 'white')
    
    # Load a font for the title
    try:
        font_path = '/path/to/your/Pacifico.ttf'  # Replace with the path to your Pacifico font
        title_font = ImageFont.truetype(font_path, size=int(72 * dpi / 72))  # Font size in pixels
    except IOError:
        title_font = ImageFont.load_default()  # Fallback
    
    # Draw title with gradient
    draw = ImageDraw.Draw(new_img)
    title_text = "Delirium 2024"
    text_width, text_height = draw.textsize(title_text, font=title_font)
    
    # Gradient overlay
    gradient = Image.new('RGB', (width_px, int(text_height * 1.5)), '#ffffff')
    gradient_draw = ImageDraw.Draw(gradient)
    
    for i in range(256):
        gradient_draw.rectangle([0, i, width_px, i+1], fill=(int(255 * (i / 255)), int(0 + 255 * (i / 255)), int(0 + 255 * (i / 255))))
    
    new_img.paste(gradient, (0, 0))
    draw.text(((width_px - text_width) / 2, (text_height / 4)), title_text, font=title_font, fill='black')
    
    # Add QR code below title
    qr_img = qr_img.resize((width_px - 40, height_px - int(text_height * 1.5) - 40))  # Resize QR code
    new_img.paste(qr_img, (20, int(text_height * 1.5) + 20))  # Position QR code

    # Save the image
    qr_code_path = f'media/qr_codes/{user.username}_qr.png'
    os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
    new_img.save(qr_code_path)
    
    return qr_code_path
