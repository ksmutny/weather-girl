from PIL import Image
import json

from netatmo_dashboard import draw_netatmo_dashboard

image = Image.new("RGB", (1200, 825), (255, 255, 255))

with open('data_netatmo.json', 'r') as file:
    data = json.load(file)

draw_netatmo_dashboard(image, 500, data)

# Transform the image to 16 shades of grey
image = image.convert('L')  # Convert to grayscale
image = image.point(lambda x: int(x / 16) * 16)  # Reduce to 16 shades

# Save the image to a PNG file
image.save("dashboard.png")
