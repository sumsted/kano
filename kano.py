import os
import serial
import json


class Kano:

    def __init__(self, debug=False):
        self.debug = debug
        self.address = self.find_device_address()
        self.device = serial.Serial(self.address)

    def pid(self, s):
        if self.debug:
            print(s)

    def close(self):
        self.device.close()

    def find_device_address(self):
        try:
            results = os.popen('dmesg |grep -i "ttyACM"| grep -i "USB ACM device"').read().split('\n')
            address =  '/dev/'+results[-2].split(' ')[-4][0:-1]
            self.pid("%s, %s"%(results[-2], address))
        except Exception:
            raise Exception('Kano device not found')
        return address

    def filter(self, unfiltered_distance):
        pass

    def read_proximity(self):
        try:
            buffer = self.device.readline()
            data = json.loads(buffer)
            proximity = 255-data['detail']['proximity']
            self.pid("proximity: %d"%proximity)
        except Exception as e:
            print(e)
        return proximity

    def command_on_threshold(self, threshold, command):
        while self.read_proximity() > threshold:
            pass
        os.system(command)


if __name__=='__main__':
    k = Kano(debug=True)
    # while True:
    # for i in range(10):
    #     print(k.read_proximity())
    k.command_on_threshold(40, 'espeak -v english-us "all your base are belong to us"')
