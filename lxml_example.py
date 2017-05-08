from lxml import html
from pprint import pprint
import requests
from io import BytesIO
from PIL import Image

URL = 'http://thecatapi.com/api/images/get?format=html&results_per_page=20'

s = requests.get(URL).content
dom = html.document_fromstring(s)


for x in dom.findall('.//img'):
    print(x.get('src'))
    im = Image.open(BytesIO(requests.get(x.get('src')).content))
    print(im.size, im.mode, im.format)