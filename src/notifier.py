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

class TwilioNotifier(Notifier):
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def notify(self, entry, score):
        message = self.client.messages.create(
            to=TWILIO_TO_NUM,
            from_=TWILIO_FROM_NUM,
            body="%s %f" % (entry['link'], score)
        )

class ConsoleNotifier(Notifier):
    def __init__(self):
        pass

    def notify(self, entry, score):
        print(entry['link'], score)
