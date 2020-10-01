import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import requests
import feedparser
from PIL import Image

from io import BytesIO
import os

from notifier import Notifier
from config import CL_RSS_FEED, MODEL_PATH, SCORE_THRESHOLD, NOTIFICATION_SERVICE

# Headers copied from Firefox for Linux v81.0
headers_xml = {
    'Host': 'sfbay.craigslist.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://sfbay.craigslist.org/search/sss?sort=date&query=chair',
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
    'Referer': 'https://sfbay.craigslist.org/search/sss?sort=date&query=chair',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

def fetch_and_test_image(url, model):
    tmp_file_name = "tmp_img.jpg"
    r = requests.get(url, headers=headers_img)

    img = Image.open(BytesIO(r.content))
    img.save(tmp_file_name)

    image_size = (150, 150)

    img = keras.preprocessing.image.load_img(
        tmp_file_name, target_size=image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)

    os.remove("./tmp_img.jpg")
    return predictions[0][0]

notifier = Notifier(NOTIFICATION_SERVICE)
r = requests.get(CL_RSS_FEED, headers=headers_xml)
if r.status_code != 200:
    notifier.notify_message(r.content)

feed = feedparser.parse(r.content)
model = keras.models.load_model(MODEL_PATH)
scores = []
for entry in feed.entries:
    try:
        score = fetch_and_test_image(entry['enc_enclosure']['resource'], model)
        if score >= SCORE_THRESHOLD:
            notifier.notify(entry, score)
    except Exception as e:
        print(e)