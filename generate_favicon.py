from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with white background
size = 192
bg_color = (255, 255, 255)  # White background
img = Image.new('RGB', (size, size), bg_color)
draw = ImageDraw.Draw(img)

# Try to use a bold font
try:
    font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 140)
except:
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 140)
    except:
        font = ImageFont.load_default()

# Draw bold "B" in black
letter_color = (0, 0, 0)  # Pure black

# Get text bounding box to center it
bbox = draw.textbbox((0, 0), "B", font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Center the text
x = (size - text_width) // 2
y = (size - text_height) // 2 - 10

draw.text((x, y), "B", font=font, fill=letter_color)

# Save as favicon
img.save("favicon.png", "PNG")
img.convert("RGB").save("favicon.ico", "ICO")

print("[OK] Favicon created successfully!")
print("[OK] favicon.png - 192x192 black B on white background")
print("[OK] favicon.ico - Favicon for browser tabs")
