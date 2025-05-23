import math
import requests
from PIL import Image, ImageDraw
from io import BytesIO

size = 512

def deg2num(ladeg, lodeg, zoom):
    n = 2 ** zoom
    xtile = int((lodeg + 180) / 360 * n) # 0, 1 (-180, 180)
    latrad = math.radians(ladeg)
    ytile = int((1 - math.log(math.tan(latrad) + 1 / math.cos(latrad)) / math.pi) / 2 * n) # mercator projection
    # https://en.wikipedia.org/wiki/Mercator_projection
    return xtile, ytile

def latlon(ladeg, lodeg, zoom):
    n = 2 ** zoom
    x = (lodeg + 180) / 360 * n * size
    latrad = math.radians(ladeg)
    y = (1 - math.log(math.tan(latrad) + 1 / math.cos(latrad)) / math.pi) / 2 * n * size # chatgpt generated math O: 
    return x, y


def download(x, y, zoom=15):
    headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.openstreetmap.org/"
    }
    url = f"https://a.basemaps.cartocdn.com/rastertiles/voyager/{zoom}/{x}/{y}@2x.png"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return (x, y), Image.open(BytesIO(r.content))
    else:
        print(f"Failed to get tile {x},{y} with status {r.status_code}")
        return (x, y), None


def genMap(lat, lon, zoom=15):
    radius = 0
    x_center, y_center = deg2num(lat, lon, zoom)
    center_px, center_py = latlon(lat, lon, zoom)
    
    coords = [(x_center + dx, y_center + dy) 
               for dx in range(-radius, radius + 1) 
               for dy in range(-radius, radius + 1)]
    
    results = []
    for x, y in coords:
        results.append(download(x, y))

    
    img_size = (2 * radius + 1) * size
    final = Image.new("RGB", (img_size, img_size))
    
    for (x, y), tile_img in results:
        if tile_img:
            px = (x - (x_center - radius)) * size
            py = (y - (y_center - radius)) * size
            final.paste(tile_img, (px, py))
    
    pinx = int(center_px - (x_center - radius) * size)
    piny = int(center_py - (y_center - radius) * size)
    
    draw = ImageDraw.Draw(final)
    r = 5
    draw.ellipse((pinx - r, piny - r, pinx + r, piny + r), fill="red", outline="white", width=2)
        
    imgb = BytesIO()    
    final.save(imgb, format="PNG")
    imgb.seek(0)
    return imgb
    
