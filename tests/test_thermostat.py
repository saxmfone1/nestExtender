from time import sleep
import unittest
from thermostat import Thermostat

class TestThermostat(unittest.TestCase):
    def setUp(self):
        self.thermostat = Thermostat("Upstairs")

    def test_heatOn(self):
        self.thermostat.heatOn()
        sleep(10)
        self.assertEqual(self.thermostat.getThermostatByName("Upstairs").hvac_state, 'heating')

    def test_heatOff(self):
        self.thermostat.heatOff()
        sleep(10)
        self.assertEqual(self.thermostat.getThermostatByName("Upstairs").hvac_state, 'off')

suite = unittest.TestLoader().loadTestsFromTestCase(TestThermostat)
unittest.TextTestRunner(verbosity=2).run(suite)