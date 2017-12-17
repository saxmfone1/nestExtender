import Adafruit_DHT
import logging
from reporter import IOLogger
from json import load
with open('./settings.json', 'r') as s:
    settings = load(s)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = IOLogger()
logger.addHandler(handler)

class Sensor:
    def __init__(self):
        sensors = {
            'AM2302': Adafruit_DHT.AM2302,
            'DHT11': Adafruit_DHT.DHT11,
            'DHT22': Adafruit_DHT.DHT22,
        }
        logger.info("Initializing sensor")
        self.sensor = sensors[settings['sensor']]
        self.pin = settings['pi_pin']
        self.offset = settings['sensor_offset']

    def getCurrentTemp(self):
        _, cTemp = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if cTemp is not None:
            fTemp = (cTemp * 1.8) + 32
            logger.info("Sensor reads {}F".format(fTemp))
            logger.info("Adding offset for calibration")
            fTemp += self.offset
            logger.info("Sensor (corrected) reads {}F".format(fTemp))
            return int(fTemp)
        else:
            logger.info("Bad reading from sensor")
            return -1