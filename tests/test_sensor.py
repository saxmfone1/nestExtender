import unittest
from sensor import Sensor

class TestSensors(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor()

    def test_getCurrentTemp(self):
        currentTemp = self.sensor.getCurrentTemp()
        self.assertEqual(type(currentTemp), int, "Did not get an integer")
        self.assertNotEqual(currentTemp, -1, "Failed to get temp")

suite = unittest.TestLoader().loadTestsFromTestCase(TestSensors)
unittest.TextTestRunner(verbosity=2).run(suite)