import nest
import sys
import logging
from reporter import Reporter
from reporter import IOLogger
from json import load
with open('./settings.json', 'r') as s:
    settings = load(s)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = IOLogger()
logger.addHandler(handler)

class Thermostat:
    def __init__(self, thermostatName):
        logger.info("Initializing thermostat {}".format(thermostatName))
        client_id = settings['nest_id']
        client_secret = settings['nest_key']
        access_token_cache_file = 'nest.json'
        self.thermostatName = thermostatName
        self.napi = nest.Nest(client_id=client_id, client_secret=client_secret,
                         access_token_cache_file=access_token_cache_file)

        if self.napi.authorization_required:
            self.printAuthMsg()

        self.thermostat = self.getThermostatByName(self.thermostatName)
        self.reporter = Reporter()

    def printAuthMsg(self):
        print('Go to ' + self.napi.authorize_url + ' to authorize, then enter PIN below')
        if sys.version_info[0] < 3:
            pin = raw_input("PIN: ")
        else:
            pin = input("PIN: ")
        self.napi.request_token(pin)

    def printDetails(self):
        for structure in self.napi.structures:
            print ('Structure %s' % structure.name)
            print ('    Away: %s' % structure.away)
            print ('    Devices:')

            for device in structure.thermostats:
                print ('        Device: %s' % device.name)
                print ('            Temp: %0.1f' % device.temperature)

        # Access advanced structure properties:
        for structure in self.napi.structures:
            print ('Structure   : %s' % structure.name)
            print (' Postal Code                    : %s' % structure.postal_code)
            print (' Country                        : %s' % structure.country_code)
            print (' num_thermostats                : %s' % structure.num_thermostats)

            # Access advanced device properties:
            for device in structure.thermostats:
                print ('        Device: %s' % device.name)
                print ('        Where: %s' % device.where)
                print ('            Mode       : %s' % device.mode)
                print ('            HVAC State : %s' % device.hvac_state)
                print ('            Fan        : %s' % device.fan)
                print ('            Fan Timer  : %i' % device.fan_timer)
                print ('            Temp       : %0.1fC' % device.temperature)
                print ('            Humidity   : %0.1f%%' % device.humidity)
                print ('            Target     : %0.1fC' % device.target)
                print ('            Eco High   : %0.1fC' % device.eco_temperature.high)
                print ('            Eco Low    : %0.1fC' % device.eco_temperature.low)

                print ('            hvac_emer_heat_state  : %s' % device.is_using_emergency_heat)

                print ('            online                : %s' % device.online)


    def getThermostats(self):
        thermostats = {}
        for structure in self.napi.structures:
            for thermostat in structure.thermostats:
                thermostats[thermostat.name] = thermostat
        return thermostats

    def getThermostatByName(self, thermostat):
        thermostats = self.getThermostats()
        return thermostats[thermostat]

    def heatOn(self):
        logger.info("Kicking on heat")
        state = self.thermostat.hvac_state
        currentTemp = self.thermostat.temperature
        if state == 'heating':
            logger.info("Heat is already on, skipping")
            pass
        else:
            logger.info("Increasing target to {}".format(currentTemp + 5))
            self.thermostat.target = currentTemp + 5

    def heatOff(self):
        logger.info("Turning off heat")
        state = self.thermostat.hvac_state
        currentTemp = self.thermostat.temperature
        if state == 'off':
            logger.info("Heat is already off, skipping")
            pass
        else:
            logger.info("Lowering heat to {}".format(currentTemp - 1))
            self.thermostat.target = currentTemp - 1

