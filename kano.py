import os
import time
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
            print(buffer)
            print(e)
        return proximity

    def do_commands(self, commands):
        max_space = 1
        threshold = 250
        code = 0
        last_seconds = 0
        new_code = True
        while True:
            proximity = self.read_proximity()
            current_seconds = time.time()
            if current_seconds - last_seconds > 1:
                if not new_code:
                    print(code)
                    # code is number of waves over kano
                    # execute command that matches code
                    try:
                        os.system(commands[code-1])
                    except Exception:
                        print("Command not found.")
                new_code = True
            else:
                new_code = False
            if proximity < threshold:
                while True:
                    proximity = self.read_proximity()
                    if proximity >= threshold:
                        code = 1 if new_code else code+1
                        last_seconds = time.time()
                        break


if __name__=='__main__':
    k = Kano(debug=False)
    # while True:
    #     k.read_proximity()
    k.do_commands([
        'espeak -v english-us "piston honda"',
        "su scott - -c firefox",
        "su scott - -c gnome-terminal",
        "su scott - -c code"
    ])