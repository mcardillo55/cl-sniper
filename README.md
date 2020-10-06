# cl-sniper

cl-sniper is a keras-based neural network model that can be trained to identify a specific item on Craigslist and provide notifications.

## Disclaimer

Craigslist is notoriously harsh on scrapers and bots. **Use reasonably and at your own risk!**

### Installation

Python dependencies can be install from the `requirements.txt` file

```sh
pip install -r ./requirements.txt
```

TensorFlow is also required, but not included in `requirements.txt`, as it is recommended to install this via your OS package manager.

### Training

You will need to provide a set of positive and negative images of the desired object. Positive images should be placed in `./src/images/yes` and negative images should be placed in `./src/images/no`.

Once the images are in place, you can train your model by running

`python ./trainer.py`

### Scanning

Once the model has been trained, `cp ./config.py.sample ./config.py`, then set the following options:

| Name            | Description                                                         |
| --------------- | ------------------------------------------------------------------- |
| CL_CITY         | The craiglist city name to scan on (e.g. 'sfbay', 'newyork')        |
| CL_RSS_FEED     | Provide the URL to the Craigslist RSS feed (note the 'query' field) |
| MODEL_PATH      | Full path to the saved epoch .h5 file during your model training    |
| KEEP_IMAGES     | Keep analyzed images (useful for retraining model)                  |
| SCORE_THRESHOLD | Float from 1.0 to 0.0 of when you would like notifcations sent      |
| TWILIO_SID      | Your Twilio SID                                                     |
| TWILIO_TOKEN    | Your Twilio Auth Token                                              |
| TWILIO_TO_NUM   | The phone number to text notifications to                           |
| TWILIO_FROM_NUM | The Twilio number to send text notifications from                   |

The scanner can then be run by issuing

`python ./scanner.py`
