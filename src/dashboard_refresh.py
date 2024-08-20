from PIL import Image
import json

from netatmo_dashboard import draw_module_data

image = Image.new("RGB", (1200, 825), (255, 255, 255))

with open('data_netatmo.json', 'r') as file:
    data = json.load(file)

room_order = [
    'Kitchen',
    'Living room',
    'Bedroom',
    "Štěpa's room",
    "Kaja's room",
    "Anička's room",
    'Bathroom',
    'Office',
    'Outdoor',
]

module_index = {}
for i, module in enumerate(data):
    module_index[module['module_name']] = i

for i, room in enumerate(room_order):
    draw_module_data(image, (60 + i * 120, 100), data[module_index[room]])


# Transform the image to 16 shades of grey
image = image.convert('L')  # Convert to grayscale
image = image.point(lambda x: int(x / 16) * 16)  # Reduce to 16 shades

# Save the image to a PNG file
image.save("dashboard.png")
