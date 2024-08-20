from PIL import Image, ImageDraw, ImageFont


font_path = "C:/Windows/Fonts/segoeui.ttf"
small_font = ImageFont.truetype(font_path, 16)
mid_font = ImageFont.truetype(font_path, 22)


def draw_module_data(image, position, module_data):
    draw = ImageDraw.Draw(image)
    (x, y) = position

    def draw_data(position, icon_name, text):
        (x, y) = position
        paste_icon((x, y), get_icon(icon_name))
        draw.text((x + 30, y), text, font=small_font, fill=(0, 0, 0))

    def draw_temperature(position, temperature):
        (x, y) = position
        draw.text((x, y), str(temperature) + ' ºC', font=mid_font, fill=black)

    def draw_co2(position, co2_level):
        if co2_level == None: return
        (x, y) = position
        paste_icon((x, y), get_co2_icon(co2_level))
        draw.text((x + 30, y), str(co2_level), font=small_font, fill=black)

    def paste_icon(position, icon):
        if (icon == None): return
        image.paste(icon, position, icon)

    black = (0, 0, 0)

    paste_icon((x + 15, y), get_room_icon(module_data['module_name']))

    draw_temperature((x, y + 110), module_data['temperature'])
    draw_co2((x, y + 160), module_data['co2'])
    draw_data((x, y + 190), 'humidity', str(module_data['humidity']) + '%')
    if module_data['pressure'] != None:
        draw_data((x, y + 220), 'pressure', str(module_data['pressure']) + ' hPa')


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
    for level in co2_icons:
        if co2_level > level:
            icon_name = co2_icons[level]
    return get_icon(icon_name)

def get_icon(icon_name):
    if icon_cache.get(icon_name) == None:
        icon_cache[icon_name] = load_icon(icon_name)
    return icon_cache[icon_name]

def load_icon(icon_name):
    return Image.open(f'icons/{icon_name}.png')
