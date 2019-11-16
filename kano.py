import os
import sys
import subprocess
import time
import serial
import json

if os.name == "nt":
    import win32com.client


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
            if os.name == 'nt':
                comp = "."
                wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator")
                swbem_services = wmi_service.ConnectServer(comp,"root\cimv2")
                all_devices = swbem_services.ExecQuery("SELECT * FROM Win32_PnPEntity")
                for device in all_devices:
                    try:
                        if "COM" in device.Name:
                            address = device.name[-5:-1]
                    except TypeError as e:
                        pass # some devices are nameless
                self.pid("%s, %s"%(device.Name, address))
            else:
                results = os.popen('dmesg |grep -i "ttyACM"| grep -i "USB ACM device"').read().split('\n')
                address =  '/dev/'+results[-2].split(' ')[-4][0:-1]
                self.pid("%s, %s"%(results[-2], address))
        except Exception as e:
            print(e)
            raise Exception('Kano device not found')
        return address

    def filter(self, unfiltered_distance):
        pass

    def read_proximity(self):
        proximity = 0
        buffer = ""
        try:
            buffer = self.device.readline()
            data = json.loads(buffer)
            proximity = 255-data['detail']['proximity']
            self.pid("proximity: %d"%proximity)
        except Exception as e:
            print(buffer)
            print(e)
        return proximity

    def exec_command(self, command):
        try:
            if os.name == 'nt':
                wrapper = "PowerShell -Command ""Start-Process -NoNewWindow '%s'"""
                subprocess.call(wrapper%command)
            else:
                id = os.fork()
                if id == 0:
                    subprocess.call(command)
                    sys.exit(0)
        except Exception as e:
            print(e)
            raise(Exception('Unable to execute command'))

    def do_commands(self, commands):
        max_delay = .5
        threshold = 250
        code = 0
        last_seconds = 0
        new_code = True
        while True:
            proximity = self.read_proximity()
            current_seconds = time.time()
            if current_seconds - last_seconds > max_delay:
                if not new_code:
                    print(code)
                    try:
                        self.exec_command(commands[code-1])
                    except Exception as e:
                        print(e)
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
        # k.read_proximity()
    k.do_commands([
        ['espeak','-v','english-us','"piston honda"'],
        ['su','scott','-','-c','firefox'],
        ['su','scott','-','-c','gnome-terminal'],
        ['su','scott','-','-c','code']
    ])

    # k.do_commands([
    #     "C:\\Program Files\\Git\\git-bash.exe",
    #     "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    #     "echo 'hello'"
    # ])