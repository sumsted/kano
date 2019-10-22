import os
import serial
import json


class Kano:

    def __init__(self):
        self.address = self.find_device_address()
        self.device = serial.Serial(self.address)

    def close(self):
        self.device.close()

    def find_device_address(self):
        results = os.popen('dmesg |grep -i "ttyACM"| grep -i "USB ACM device"').read().split('\n')
        for line in reversed(results[0:-1]):
            print('line: %s' % line)
            device = '/dev/'+line.split(' ')[-4][0:-1]
            break
        return device

    def filter(self, unfiltered_distance):
        pass

    def read_distance(self):
        distance = 0
        try:
            buffer = self.device.readline()
            data = json.loads(buffer)
            proximity = data['detail']['proximity']
            factor = 5
            distance = (255-proximity)**factor * 40 / (255**factor) + 5
        except Exception as e:
            print(e)
        return distance


if __name__=='__main__':
    k = Kano()
    while True:
        print(k.read_distance())