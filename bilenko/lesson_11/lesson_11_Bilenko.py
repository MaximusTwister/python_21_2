import requests
import os
import shutil
from threading import Thread
from datetime import datetime
import urllib.request

key = '23023137-d9a069bf9dfce13f705eba7e2'
url = 'https://pixabay.com/api/videos/'
directory = './videos/'
params = {'key': key, 'q': 'dog'}


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        func(*args)
        return datetime.now()-start_time
    return wrapper


def download_video(hit):
    hit_url = hit.get('videos').get('large').get('url')
    hit_id = hit.get('id')
    res = requests.get(hit_url)
    urllib.request.urlretrieve(hit_url, f'{directory}test_{hit_id}.mp4')



@timer
def download_videos(n):
    threads = []
    res = requests.get(url=url, params=params)
    hits = res.json().get('hits')
    for img_num in range(n):
        threads.append(Thread(target=download_video, args=(hits[img_num],)))
        r = [th.start for th in threads]
        print(r)

@timer
def download_videos2(n):
    res = requests.get(url=url, params=params)
    hits = res.json().get('hits')
    for img_num in range(n):
        download_video(hits[img_num])


print(f'threads method is {download_videos(3)}\nnormal method is {download_videos2(3)}')



