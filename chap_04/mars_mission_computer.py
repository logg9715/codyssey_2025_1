# mars_mission_computer.py

import time
import json
import threading

class DummySensor:
    def get_internal_temperature(self):
        return 21.5

    def get_external_temperature(self):
        return -55.3

    def get_internal_humidity(self):
        return 35.2

    def get_external_illuminance(self):
        return 1200.0

    def get_internal_co2(self):
        return 400.0

    def get_internal_oxygen(self):
        return 20.9

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        self.history = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': []
        }
        self.ds = DummySensor()
        self.running = True

    def get_sensor_data(self):
        start_time = time.time()

        while self.running:
            self.env_values['mars_base_internal_temperature'] = self.ds.get_internal_temperature()
            self.env_values['mars_base_external_temperature'] = self.ds.get_external_temperature()
            self.env_values['mars_base_internal_humidity'] = self.ds.get_internal_humidity()
            self.env_values['mars_base_external_illuminance'] = self.ds.get_external_illuminance()
            self.env_values['mars_base_internal_co2'] = self.ds.get_internal_co2()
            self.env_values['mars_base_internal_oxygen'] = self.ds.get_internal_oxygen()

            for key in self.env_values:
                self.history[key].append(self.env_values[key])
                if len(self.history[key]) > 60:
                    self.history[key].pop(0)

            print(json.dumps(self.env_values, indent=4))

            if time.time() - start_time >= 300:
                print('--- 5분 평균 ---')
                for key, values in self.history.items():
                    if values:
                        average = sum(values) / len(values)
                        print(key + ': ' + str(round(average, 2)))
                print('----------------')
                start_time = time.time()

            time.sleep(5)

    def stop(self):
        self.running = False
        print('System stopped....')

def input_listener(mc):
    while mc.running:
        user_input = input()
        if user_input.strip().lower() == 'q':
            mc.stop()

if __name__ == '__main__':
    RunComputer = MissionComputer()
    input_thread = threading.Thread(target=input_listener, args=(RunComputer,))
    input_thread.daemon = True
    input_thread.start()
    RunComputer.get_sensor_data()
