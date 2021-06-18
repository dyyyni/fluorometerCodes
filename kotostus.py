import os
import sys

import nidaqmx as ni

import win32gui
import win32com.client
import time
import traceback

# globals
task = None
exit_flag = False
wrt_file = None
counts_prev = None
counts_now = None
interval = 1

def clear_screen():

    os.system('cls')

    return

def start_ni_device():
# This function is set up to start the DAQ-card.
# Function checks if a NI-device is connected to the computer.
# You can see the name of your device in the NI-MAX software if it matters to you.

    global task

    devices = ni.system.system.System.local().devices
    if devices.__len__() < 1:
        print('No NI device detected. Aborting program execution.')
        sys.exit(1)

    name = devices[0].name + '/ctr1'
    if devices.__len__() > 1:
        print('Multiple NI devices detected. Using device/channel \'' + name + '\'')

    if devices.__len__() == 1:
        print('NI device detected. Using device/channel \'' + name + '\'')

    task = ni.Task('digital readout')
    task.ci_channels.add_ci_count_edges_chan(name)
    task.start()

    return

def stop_ni_device():
    task.stop()
    task.close()
    #wrt_file.close()

    return

def start_pulsar():

    global OphirCOM

    OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
     # Stop & Close all devices
    OphirCOM.StopAllStreams() 
    OphirCOM.CloseAll()
    # Scan for connected Devices
    DeviceList = OphirCOM.ScanUSB()
    
    if len(DeviceList) < 1:
        print('Pulsar is not detected. Aborting program execution.')
        sys.exit(1)
    else: print('Pulsar detected.')

    return

def stop_pulsar():

    global OphirCOM
    
    # Stop & Close all devices
    OphirCOM.StopAllStreams()
    OphirCOM.CloseAll()
    # Release the object
    OphirCOM = None


def main():

    clear_screen()

    # NI-device setup
    #start_ni_device()
    #stop_ni_device()

    # Pulsar setup
    start_pulsar()
    stop_pulsar()

    return


if __name__ == '__main__': main()
