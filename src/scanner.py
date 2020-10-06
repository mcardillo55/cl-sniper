import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import requests
import feedparser
from PIL import Image

from datetime import datetime
from io import BytesIO
import os
import pickle
import time
import random
import multiprocessing

from notifier import Notifier
from config import KEEP_IMAGES, CL_RSS_FEED, CL_CITY, MODEL_PATH, SCORE_THRESHOLD, NOTIFICATION_SERVICE

# Headers copied from Firefox for Linux v81.0
headers_xml = {
    'Host': f'{CL_CITY}.craigslist.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': f'https://{CL_CITY}craigslist.org/search/sss?sort=date&query=chair',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

headers_img = {
    'Host': 'images.craigslist.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': f'https://{CL_CITY}.craigslist.org/search/sss?sort=date&query=chair',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

notifier = Notifier(NOTIFICATION_SERVICE)

def fetch_and_test_image(url, model):
    img_path = os.path.join('images', url.split('/')[-1])
    r = requests.get(url, headers=headers_img)

    img = Image.open(BytesIO(r.content))
    img.save(img_path)

    image_size = (256, 256)

    img = keras.preprocessing.image.load_img(
        img_path, target_size=image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)

    if not KEEP_IMAGES:
        os.remove(img_path)
    return predictions[0][0]

def scan():
    print("[%s] starting analysis..." % (datetime.now()))

    r = requests.get(CL_RSS_FEED, headers=headers_xml)
    if r.status_code != 200:
        notifier.notify_message(r.content)

    # Load in previously analyzed URLs
    seen_filename = 'seen.pkl'
    try:
        with open(seen_filename, 'rb') as f:
            seen = pickle.load(f)
    except FileNotFoundError:
        seen = {}

    feed = feedparser.parse(r.content)
    model = keras.models.load_model(MODEL_PATH)
    matches = []
    for entry in feed.entries:
        if entry['link'] not in seen:
            try:
                score = fetch_and_test_image(entry['enc_enclosure']['resource'], model)
                if score >= SCORE_THRESHOLD:
                    matches.append((entry, score))     
            except Exception as e:
                print(e)
            seen[entry['link']] = datetime.now()
    notifier.notify(matches)

    # Save dict of analyzed URLs for next run
    with open(seen_filename, 'wb') as f:
        pickle.dump(seen, f)

while True:
    p = multiprocessing.Process(target=scan) # Run scan() in separate process to free up GPU memory while sleeping
    p.start()
    p.join()

    sleep_time = 60*15+random.randint(1,60*15)
    print("sleeping for %f minutes." % (sleep_time / 60.0))
    time.sleep(sleep_time)