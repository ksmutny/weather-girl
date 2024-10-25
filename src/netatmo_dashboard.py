from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


font_path = "font/segoeui.ttf"
small_font = ImageFont.truetype(font_path, 16)
mid_font = ImageFont.truetype(font_path, 26)

black = (0, 0, 0)
grey = (128, 128, 128)

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

def draw_netatmo_dashboard(image, y, data):
    module_index = {}
    for i, module in enumerate(data):
        module_index[module['module_name']] = i

    draw = ImageDraw.Draw(image)
    tile_width = module_tile_width(draw)
    tile_count = len(room_order)
    gap = (image.width - tile_width * tile_count) // (tile_count + 1)

    for i, room in enumerate(room_order):
        draw_module_data(image, (gap + i * (tile_width + gap), y), tile_width, data[module_index[room]])

    updated = datetime.now().strftime('%d.%m. %H:%M')
    draw.text((image.width - 100, y + 290), updated, font=small_font, fill=grey)


def draw_module_data(image, position, tile_width, module_data):
    (x, y) = position
    draw = ImageDraw.Draw(image)

    def draw_room_icon(room_name):
        paste_icon((x + (tile_width - 60) // 2, y), get_room_icon(room_name))

    def paste_icon(position, icon):
        if (icon == None): return
        image.paste(icon, position, icon)

    def print_d(delta, key, unit = '', font = small_font, icon = None):
        if module_data[key] == None: return

        icon = get_icon(key) if icon == None else icon
        icon_width = 0 if icon == None else 30
        paste_icon((x, y + delta), icon)

        text = str(module_data[key])
        text_width = draw.textbbox((0, 0), text, font=font)[2]
        draw.text((x + icon_width, y + delta), text, font=font, fill=black)
        draw.text((x + icon_width + text_width, y + delta), unit, font=font, fill=grey)

    draw_room_icon(module_data['module_name'])

    print_d(110, 'temperature', ' ºC', font = mid_font)
    print_d(160, 'co2', icon = get_co2_icon(module_data['co2']))
    print_d(190, 'humidity', '%')
    print_d(220, 'pressure', ' hPa')



def module_tile_width(draw):
    return draw.textbbox((0, 0), '88.8 ºC', font=mid_font)[2]

icon_cache = {}

room_icons = {
    'Kitchen': 'room-kitchen',
    'Living room': 'room-living-room',
    'Bathroom': 'room-bathroom',
    'Bedroom': 'room-bedroom',
    'Office': 'room-office',
}

def get_room_icon(room_name):
    icon_name = room_icons.get(room_name)
    if icon_name: return get_icon(icon_name)
    return None

co2_icons = {
       0: 'co2-light',
     500: 'co2-dark',
    1000: 'co2-black',
    2000: 'co2-bck',
}

def get_co2_icon(co2_level):
    if co2_level == None: return None
    for level in co2_icons:
        if co2_level > level:
            icon_name = co2_icons[level]
    return get_icon(icon_name)

def get_icon(icon_name):
    if icon_cache.get(icon_name) == None:
        icon_cache[icon_name] = load_icon(icon_name)
    return icon_cache[icon_name]

def load_icon(icon_name):
    try:
        return Image.open(f'icons/{icon_name}.png')
    except FileNotFoundError:
        return None
