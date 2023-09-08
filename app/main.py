

from fastapi import FastAPI, Response
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests

app = FastAPI()

base_image_path = './image.png'
font_path = './Roboto-Regular.ttf'
color = '#2D2E3A'
font_32 = ImageFont.truetype(font_path, 32)
font_24 = ImageFont.truetype(font_path, 24)
font_16 = ImageFont.truetype(font_path, 16)
font_12 = ImageFont.truetype(font_path, 12)
address_label = "Inatatsu Address"
node = 'https://sym-main-03.opening-line.jp:3001'

@app.get("/")
def read_root():
    return {"Hello": "Hello Flask"}

@app.get("/account/{addr}")
def getImage(addr):
    base_image = Image.open(base_image_path).resize((560, 234))

    draw = ImageDraw.Draw(base_image)

    response = requests.get(node + '/accounts/' + addr)
    account = response.json()["account"]

    token_count = len(account["mosaics"]) - 1
    and_more = f'and {token_count} other mosaics'
    xym_label = 'XYM'
    xym_str = account['mosaics'][0]['amount']
    xym = xym_str[:-6] + '.' +xym_str[-6:]



    draw.text((50, 50), address_label, font=font_24, fill=color)
    draw.text((50, 90), addr, font=font_16, fill=color)

    draw.text((50, 120), xym_label, font=font_32, fill=color)
    draw.text((140, 120), xym, font=font_32, fill=color)
    draw.text((50, 165), and_more, font=font_16, fill=color)

    img_bytes = BytesIO()
    base_image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    response = Response(content=img_bytes, media_type="image/png")
    response.headers["Cache-Control"] = "max-age=0"
    return response
