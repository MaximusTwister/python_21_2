import os
import requests
import shutil
from datetime import datetime
from threading import Thread
from tqdm import tqdm


video_endpoint = 'https://pixabay.com/api/videos/'
#api_key = os.environ['API_KEY_PIXABEY']
api_key = '23023135-2d931c53425ba0ca1d345b34e'


# Decorator
def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        end = datetime.now()
        total_time = end - start
        return total_time

    return wrapper


# Get category of video from user input
def get_user_input_category():
    while True:
        category = input('Enter category of videos for downloads:\n➜ ')
        if video_category(params={'q': category, 'key': api_key}) and category.isalpha():
            return category
        else:
            print(f'\n🤷‍ Unfortunately we do not find the video category: {category}. '
                  f'Check your spell 📝 or try another one')


def video_category(params):
    res = requests.get(url=video_endpoint, params=params)
    try:
        res.raise_for_status()
        return res.json()['hits']
    except requests.exceptions.HTTPError:
        return None


# Get number of video for download from user input
def get_user_input_quantity_video(category):
    while True:
        num_of_video = input('Enter number of videos for downloads:\n➜ ')
        q_video = quantity_video(params={'q': category, 'key': api_key})
        if num_of_video.isdigit():
            if q_video >= int(num_of_video):
                return int(num_of_video)
            else:
                print(f'\n🤷‍ Unfortunately we do not have that many videos for download: {num_of_video}.\n'
                      f'We have only {q_video} videos for download'
                      f'Download {q_video} videos started')
                num_of_video = q_video
                return num_of_video
        else:
            print(f'\nYou entered not number: {num_of_video}. '
                  f'Check your spell 📝 or try another one')


def quantity_video(params):
    res = requests.get(url=video_endpoint, params=params)
    return res.json()['total']


#Download one video
def download_video(hit):
    hit_video_url = hit.get('videos').get('medium').get('url')
    videoname_from_url = hit_video_url.split('?')[0]
    videoname_from_url = videoname_from_url.split('/')[-1]
    res = requests.get(url=hit_video_url, stream=True)
    with open(f'./videos/{videoname_from_url}', 'wb') as file:
        for chunk in res.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f' {videoname_from_url} was successfully saved')


# Download videos use one thread
@timeit
def download_videos(quantity, params):
    res = requests.get(url=video_endpoint, params=params)
    hits = res.json()['hits']
    for video_num in tqdm(range(quantity)):
        download_video(hits[video_num])


# Download videos use many thread
@timeit
def download_videos_threads(quantity, params):
    threads = list()
    res = requests.get(url=video_endpoint, params=params)
    hits = res.json()['hits']
    for video_num_th in tqdm(range(quantity)):
        threads.append(Thread(target=download_video, args=(hits[video_num_th],)))
        for th in threads:
            if not th.is_alive():
                th.start()


# Run programm and contain all necessary parameters
def main():
    category = get_user_input_category()
    quantity = get_user_input_quantity_video(category)

    params = {
        'q': category,
        'key': api_key,
        'videos': 'medium',
        'download': 1,
    }

    path = './videos'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    time_one_thread = download_videos(quantity, params)
    print(f'File upload time using one thread: {time_one_thread}')

    path = './videos'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    time_many_thread = download_videos_threads(quantity, params)
    print(f'File upload time using {quantity} threads: {time_many_thread}')


# Entrypoint
main()
