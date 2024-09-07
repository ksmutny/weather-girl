from PIL import Image
from fs_json import read_json

from netatmo_dashboard import draw_netatmo_dashboard

image = Image.new("RGB", (1200, 825), (255, 255, 255))

data = read_json('data_netatmo.json')

draw_netatmo_dashboard(image, 500, data)

# Transform the image to 16 shades of grey
image = image.convert('L')  # Convert to grayscale
image = image.point(lambda x: int(x / 16) * 16)  # Reduce to 16 shades

# Save the image to a PNG file
image.save("dashboard.png")
