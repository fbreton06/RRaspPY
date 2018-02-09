#!/usr/bin/env python
import types
from subprocess import Popen, PIPE, STDOUT

class Debug(object):
    VERBOSITY = ("Unknown", "NONE", "INFO", "ERROR", "DETAIL", "DEBUG", "DUMP")
    NONE = 1
    INFO = 2
    ERROR = 3
    DETAIL = 4
    DEBUG = 5
    DUMP = 6
    def __init__(self,  level=NONE):
        assert level > 0, "Unexpected debug level value: %s" % level
        self.debug_level = level

    def isLevel(self, level):
        return self.debug_level >= level

    def getVerbosity(self):
        try:
            return self.VERBOSITY[self.debug_level]
        except:
            return self.VERBOSITY[0]

    def getHexStream(self, stream, sep=" "):
        return sep.join(["%02X" % ord(x) for x in stream])

    def TAG(self, level, name, width=25, deco='#'):
        if self.isLevel(level):
            print deco * width + ' ' + name + ' ' + deco * width

    def TRACE(self, level, *args):
        if self.isLevel(level):
            if type(args[0]) in types.StringTypes:
                print args[0] % args[1:],
            else:
                print " ".join([str(x) for x in args]),

    def DUMPHEX(self, text, stream, sep=" ", level=DUMP):
        if self.isLevel(level):
            print text + self.getHexStream(stream, sep)

def GetIPAddress(networkName):
    # Linux stuff (of course unusable with Windows system)
    command = "ip addr show %s | awk -F\" +|/\" 'NR==3{print $3}'" % networkName
    process = Popen(command, stdout=PIPE, shell=True, stderr=STDOUT)
    result = process.communicate()
    if result[0].count(".") != 3:
        raise ValueError, "wlan0 IP address is not found: \"%s\"" % result[0]
    return result[0].strip()

if __name__ == "__main__":
    dbg = Debug(Debug.DETAIL)
    dbg.TAG(Debug.DEBUG, "test")
    dbg.TRACE(Debug.DETAIL, "Format %s\n",  "OK!")
    dbg.TRACE(Debug.DETAIL, 25, 12, 23.0, "\n")
    dbg.DUMPHEX("Test: ", "0123456789", "-", Debug.DETAIL)
    dbg.TAG(Debug.INFO, "done", 10, '!')
    raw_input("Appuyer sur entree pour continuer")

