from sensor import Sensor
from thermostat import Thermostat
from reporter import Reporter
from reporter import IOLogger
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = IOLogger()
logger.addHandler(handler)


class Extender:
    def __init__(self, thermostatName, target):
        logger.info("Initializing extender")
        self.sensor = Sensor()
        self.thermostat = Thermostat(thermostatName)
        self.reporter = Reporter()
        self.target = target

    def startPoller(self, interval):
        logger.info("Starting poller")
        while True:
            try:
                self.poll()
            except Exception as e:
                logger.error("Could not complete run: {}".format(e.message))
            logger.info("Sleeping for {} seconds".format(interval))
            sleep(interval)

    def poll(self):
        temperature = self.sensor.getCurrentTemp()
        thermostatTarget = self.thermostat.thermostat.target
        thermostatTemp = self.thermostat.thermostat.temperature
        self.reporter.send('thermostat_target', thermostatTarget)
        self.reporter.send('thermostat_temp', thermostatTemp)
        self.reporter.send('sensor_temp', temperature)
        if temperature == -1:
            logger.info("Got a bad reading from the sensor, try again later")
            pass
        elif temperature >= self.target:
            logger.info("Temperature was hot enough")
            self.thermostat.heatOff()
        else:
            logger.info("Temperature was too cold")
            self.thermostat.heatOn()
