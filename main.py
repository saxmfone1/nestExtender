from extender import Extender
from json import load
with open('./settings.json', 'r') as s:
    settings = load(s)

def main():
    extender = Extender(settings['thermostat_name'], settings['target_temp'])
    extender.startPoller(settings['poll_interval'])

if __name__ == "__main__":
    main()
