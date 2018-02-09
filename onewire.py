#!/usr/bin/env python
import os, time
from helper import *
import host

host.ImportModule("os")

verbosity = Debug.ERROR
#verbosity = Debug.DEBUG

class OneWire(Debug):
    def __init__(self, number=""):
        Debug.__init__(self, verbosity)
        if number:
            device = "/sys/bus/w1/devices/%s/w1_slave" % number
            if not host.Execute("os.path.isfile(\"%s\")" % device):
                raise ValueError, "1-Wire device %s not detected!" % device
        else:
            # Autodetection
            device = ""
            for number in host.Execute("os.listdir(\"/sys/bus/w1/devices\")"):
                if number != 'w1_bus_master1':
                    device = "/sys/bus/w1/devices/%s/w1_slave" % number
                    break
            if device == "":
                raise ValueError, "1-Wire Probe not auto-detected!"
        try:
            bus = host.Execute("open(\"%s\")" % device)
            host.Execute("close()", bus)
            host.RemoveHandle(bus)
        except:
            raise ValueError, "1-Wire device %s: unexpected error!" % device
        self.__device = device

    def read(self):
        bus = host.Execute("open(\"%s\")" % self.__device)
        data = host.Execute("read()", bus)
        host.Execute("close()", bus)
        host.RemoveHandle(bus)
        return data

    def write(self, data):
        bus = host.Execute("open(\"%s\")" % self.__device)
        host.Execute("write(\"%s\")" % str(data), bus)
        host.Execute("close()", bus)
        host.RemoveHandle(bus)
