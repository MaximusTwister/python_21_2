import requests
from requests_toolbelt import MultipartEncoderMonitor, MultipartEncoder
from tqdm import tqdm
from time import sleep


url = 'http://httpbin.org'


def my_callback(monitor):
    for i in tqdm(range(int(100))):
        sleep(0.01)


files = [('image', ('nature.jpg', open('nature.jpg', 'rb'), 'image/png')),
         ('image', ('field.jpg', open('field.jpg', 'rb'), 'image/png')),
         ('image', ('mountings.jpg', open('mountings.jpg', 'rb'), 'image/png')),
         ('image', ('city.jpg', open('city.jpg', 'rb'), 'image/png')),
         ('image', ('cat.jpg', open('cat.jpg', 'rb'), 'image/png')),
         ('image', ('waterfall.jpg', open('waterfall.jpg', 'rb'), 'image/png'))]


payload = MultipartEncoder(fields=files)
monitor = MultipartEncoderMonitor(payload, my_callback)

r = requests.post(f'{url}/post', data=monitor)
