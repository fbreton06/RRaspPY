# RRaspPY
Python 2.7 package to be able to run python software from a host machine connected to the a Raspberry Pi device


How to use:
1) You should first get the package on your host machine.
I've only tested it on Ubuntu64 system but it should work on other system like Windows or any else.
2) Copy to your raspbery device the following set of files in a folder anywhere in your system but of course with grant access:
  - helper.py
  - serialize.py
  - common.py
  - device.py
3) From your raspberry (probably throught your SSH connection) just start the server like that:
$> python ./server.py HOST_ADDRESS [DEVICE_ADDRESS] [HOST_PORT=7070] [DEVICE_PORT=8080]
Where:
  - HOST_ADDRESS              It should be IP address of the network interface used by your host to execute you python application.
  - DEVICE_ADDRESS [optional] By default on linux system it is the IP address of the "eth0" interface
                              It should be the interface used by your raspberry to expose the server.
                              Probably something like: wlan0 or eth0... for linux based system.
                              If the detection doesn't work you could enter directly the IP address of the network interface
  - HOST_PORT      [optional] Is the port number used by the host
  - DEVICE_PORT    [optional] Is the port number used by the raspberry server

4) You need to do the same thing dirrectly in the host.py file:
    HOST_TUPLE = (HOST_ADDRESS, 7070)
    DEVICE_TUPLE = (DEVICE_ADDRESS, 8080)
local variable should be False. It exists only to test/debug mechanism with DEVICE/HOST couple on the same machine.

5) After that you could run your python script from any python interpreter like it was located on your raspberry.
(Personally I recommand PyScripter for Windows users or Wing for all users especially if you debug multi-threading code)
Of course to be able to do that all interfaces that you'll use should be simulated by your host throught commands located in the host module.
For the moment SMBus, RPi.GPIO and Adafruit_ADS1x15 are supported.
Feel free to improve this set of hardware support. E.g. Adafruit_ADS1x15 support actually only the ADS1115, but it'll be easy to add the
ADS1015 chip support. 
Maybe you'll encounter few issues with variables that is not defined by the RPi.GPIO stub. But in the most of case it should work.


How it work:
  Host communicate with device by two client/server socket mechanism. A lot of threads are used...
  The device server wait command from the host. Mainly "import" and "execute" commands.
  - "import" command will do what do the python "import module"
  - "execute" command will execute any python command that could be interpreted by the python eval() command
  Some stuff has been added to manage instance of object and callback mechanism.
  
  Then to support callback mechanism, a server is present in the host side to manage them.


Understand how add a new hardware support:
The smbus.py file is a good sample to start.
1) import host
    You need to import host module to be able to communicate with the device side (raspberry server)
2) host.ImportModule("smbus")
    This line will execute "import smbus" command in the device context
3) bus = host.Execute("smbus.SMBus(1)")
    This line will execute "bus = smbus.SMBus(1)" command in the device context and returns a number that is an handle on your instance.
4) host.Execute("read_byte(0x33)", bus)
    This line will execute "bus.read_byte(0x33)" command in the device context and returns the bytes string read.
5) At the end host.RemoveHandle(bus) is called to clean remote instance

Files descriptions:
  - helper.py       Contains useful class or function for the module
  - serialize.py    Dedicated to Encode/Decode stream to/from socket
  - common.py       Just common definitions between the host and the device sides
  - device.py       Execute "host" command in the device context and send callback event to the "host"
  - host.py         Send commands to the device and listening callback event
  
The most of them have autotest to check their content: (see __name__=="__main__" section at the bottom of the code)
