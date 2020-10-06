from twilio.rest import Client
from config import TWILIO_SID, TWILIO_TOKEN, TWILIO_TO_NUM, TWILIO_FROM_NUM

class Notifier(object):
    def __init__(self, service):
        if service == "twilio":
            self.notifier = TwilioNotifier()
        else:
            self.notifier = ConsoleNotifier()

    def notify(self, matches):
        self.notifier.notify(matches)

    def notify_message(self, message):
        self.notifier.notify_message(message)

class TwilioNotifier(Notifier):
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def notify(self, matches):
        notify_string = ""
        for entry, score in matches:
            notify_string += "%s %.4f\n" % (entry['link'], score)
        if matches:
            self._send_sms(notify_string)

    def notify_message(self, message):
        self._send_sms(message)

    def _send_sms(self, message):
        MAX_SIZE = 1500 # Max Twilio message size is 1600, but some characters are larger so we use 1500 to be safe

        # Split message into messages that are MAX_SIZE characters long (if it's larger, which should be rare)
        for idx, split_message in enumerate([message[i:i+MAX_SIZE] for i in range(0, len(message), MAX_SIZE)]):
            self.client.messages.create(
                to=TWILIO_TO_NUM,
                from_=TWILIO_FROM_NUM,
                body=split_message
            )

class ConsoleNotifier(Notifier):
    def __init__(self):
        pass

    def notify(self, matches):
        for entry, score in matches:
            print(entry['link'], score)

    def notify_message(self, message):
        print(message)