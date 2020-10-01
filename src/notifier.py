from twilio.rest import Client
from config import TWILIO_SID, TWILIO_TOKEN, TWILIO_TO_NUM, TWILIO_FROM_NUM

class Notifier(object):
    def __init__(self, service):
        if service == "twilio":
            self.notifier = TwilioNotifier()
        else:
            self.notifier = ConsoleNotifier()

    def notify(self, entry, score):
        self.notifier.notify(entry, score)

    def notify_message(self, message):
        self.notifier.notify_message(message)

class TwilioNotifier(Notifier):
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def notify(self, entry, score):
        self._send_sms("%s %f" % (entry['link'], score))

    def notify_message(self, message):
        self._send_sms(message)

    def _send_sms(self, message):
        message = self.client.messages.create(
            to=TWILIO_TO_NUM,
            from_=TWILIO_FROM_NUM,
            body=message
        )

class ConsoleNotifier(Notifier):
    def __init__(self):
        pass

    def notify(self, entry, score):
        print(entry['link'], score)

    def notify_message(self, message):
        print(message)