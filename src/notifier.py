class Notifier(object):
    def __init__(self, service):
        if service == "console":
            self.notifier = ConsoleNotifier()
        else:
            self.notifier = ConsoleNotifier()

    def notify(self, entry, score):
        self.notifier.notify(entry, score)

class ConsoleNotifier(Notifier):
    def __init__(self):
        pass

    def notify(self, entry, score):
        print(entry['link'], score)
