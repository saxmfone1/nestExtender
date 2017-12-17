from Adafruit_IO import Client
from logging import Handler
from json import load
with open('./settings.json', 'r') as s:
    settings = load(s)

class Reporter:
    def __init__(self):
        key = settings['aio_key']
        self.aio = Client(key)

    def send(self, feed, value):
        return self.aio.send(feed, value)

class IOLogger(Handler):
    def emit(self, record):
        aio = Reporter()
        log_entry = self.format(record)
        return aio.send('log', log_entry)