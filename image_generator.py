# This file is used to generate the wall paper  for oppo find x5 pro 1440 x 3216 pixels

# For a year, we have 365 dots. do 15 wide,

# Create a blank canvas using Pillow
from PIL import Image, ImageDraw, ImageFont
import json
import textwrap
from datetime import date, time, datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# Variables for image gen
scale = 2
image_size = [1440*scale, 3216*scale]
radius = 20*scale
num_dots_x = 15
num_dots_y = 25
days = 365
margin_x = 200 * scale
margin_y = 900 * scale
usable_width = image_size[0] - 2*margin_x #1040
usable_height = 1700 * scale
gap = usable_width/ (num_dots_x - 1)
gap_y = usable_height/(num_dots_y -1)

# Colour Variables
bg_colour = (18, 16, 14)
colour = (210, 220, 220)
yellow_colour = (212, 175, 55)
dark_grey_colour = (70, 65, 60)

# Font
base_path = Path(__file__).parent
font_path = base_path / "font" / "static" / "PlayfairDisplay-Black.ttf"
font_small = ImageFont.truetype(str(font_path), 52 * scale)
font_large = ImageFont.truetype(str(font_path), 100 * scale)

# Create new instance of image and Draw
new_image = Image.new("RGB", image_size, color=bg_colour)
draw = ImageDraw.Draw(new_image)

# Date Variables
# today = date.today() #Commeting this out as when running on github actions its in UTC time
today = datetime.now(ZoneInfo("Australia/Sydney")).date()
year_start = date(today.year, 1, 1)
day_of_year = (today - year_start).days + 1
precentage = round((day_of_year / 365)*100)
day_count = 0

# Dot generation
for j in range(num_dots_y):
    current_row_width = 5 if j == 24 else num_dots_x
    for i in range(current_row_width):
        x_pos = margin_x + i*gap
        y_pos = margin_y  + j*gap_y
        day_count += 1
        if day_count == day_of_year:
            colour = yellow_colour
            # continue
        elif day_count > day_of_year:
            colour = dark_grey_colour
        draw.circle((x_pos, y_pos), radius, outline=colour, fill=colour)


# Text generation
quote_base = margin_y + usable_height
draw.text((new_image.width/2, quote_base), text=str(day_of_year)+"/365 "+f"({precentage}%)", font=font_small, fill=yellow_colour, anchor="mm", stroke_width=2)
# quote = "This is your year, achieve your goals"
# draw.text((new_image.width/2, quote_base + 100), text=quote, font=font_small, fill=yellow_colour, anchor="mm", stroke_width=1)

try:
    with open("quotes.json", "r") as f:
        data = json.load(f)
        quotes = data["quotes"]
        quote = quotes[(today.toordinal()) % len(quotes)]
        print(quote)
except FileNotFoundError:
    print("file not found")

# Wrap the text to a specified width & join the list of lines with newline characters
wrapped_lines = textwrap.wrap(quote, width=27)
text_with_newlines = "\n".join(wrapped_lines)
draw.multiline_text((new_image.width/2, quote_base + 200*scale), text=text_with_newlines, font=font_large, fill=yellow_colour, anchor="mm", stroke_width=2, spacing=20)

new_image.show()
new_image = new_image.resize((1440, 3216), Image.LANCZOS)
new_image.save("wallpaper.png", quality=100)






