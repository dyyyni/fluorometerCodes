'''
******************************************************************************
Optonome controller V2
Creator : Daniel Luoma | daniel.luoma@tuni.fi

This software controls the optonome project measuring device data acquisition.

The main functionality of the program i
******************************************************************************
'''

import os
import sys
import time

import nidaqmx as ni
import win32com.client

# globals
task = None
wrt_file = None
counts_prev = None
counts_now = None
pulsarReading = None
isNi = False
isPulsar = False
n_measurements = 0
interval = 1 # Measuring interval. Set to 1 measurement/second


def prepare_file():

    global wrt_file
    global save_path

    fileName = input('Enter the filename: ')
    save_path = os.getcwd() + '\\' + fileName + '.csv'
    sys.stdout.write('Saving data to \'' + save_path + '\n\nInitialising...\n')
    wrt_file = open(save_path, 'w')
    wrt_file.write('sep=,\n')
    wrt_file.write('Counts(#/s),Power(W),Time(s)\n')

    return

def exit_program():
    # Safe way to terminate the program

    global save_path
    global isPulsar
    global isNi

    print('\n*********************************************')
    print('Exiting Program..\n')
    if isNi: stop_ni_device()
    if isPulsar: stop_pulsar()
    wrt_file.close()

    print('\nData file saved succesfully to ' + save_path)

    print('\nProgram Finished.')
    print('*********************************************')

    sys.exit(1)

def clear_screen():

    os.system('cls')

    return

def start_ni_device():
# This function is set up to start the DAQ-card.
# Function checks if a NI-device is connected to the computer.
# You can see the name of your device in the NI-MAX software if it matters to you.

    global task
    global isNi

    devices = ni.system.system.System.local().devices
    if devices.__len__() < 1:
        print('No NI device detected. Aborting program execution.')
        exit_program()

    name = devices[0].name + '/ctr1'
    if devices.__len__() > 1:
        print('Multiple NI devices detected. Using device/channel \'' + name + '\'')

    if devices.__len__() == 1:
        print('NI device detected. Using device/channel \'' + name + '\'')

    isNi = True

    task = ni.Task('digital readout')
    task.ci_channels.add_ci_count_edges_chan(name)
    task.start()

    return

def stop_ni_device():

    task.stop()
    task.close()

    print('NI device deactivated succesfully.')

    return

def read_PMTcounts():

    global n_measurements
    global counts_now

    counts_now = task.ci_channels[0].ci_count

    return

def start_pulsar():

    global OphirCOM
    global DeviceHandle
    global Device
    global isPulsar

    OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
     # Stop & Close all devices
    OphirCOM.StopAllStreams() 
    OphirCOM.CloseAll()
    # Scan for connected Devices
    DeviceList = OphirCOM.ScanUSB()
    
    if len(DeviceList) < 1:
        print('Pulsar is not detected. Aborting program execution.')
        exit_program()
    else: 
        isPulsar = True
        print('Pulsar detected.')

    for Device in DeviceList:   	# if any device is connected
        DeviceHandle = OphirCOM.OpenUSBDevice(Device)	# open first device
        exists = OphirCOM.IsSensorExists(DeviceHandle, 0)
        if exists:
            print('\nThe active power sensor setup:')

    setup_pulsar()

    OphirCOM.StartStream(DeviceHandle, 0)		# start measuring

    return

def setup_pulsar():
    # The sensor setup : (1) Filter is out, (2) Wavelength 365nm and  (3) Range : 300uW

    getFilter = OphirCOM.GetFilter(DeviceHandle, 0)
    filterPosition = getFilter[0]
    print('(1) The filter is set to position: ' + getFilter[1][filterPosition])

    getWavelengths = OphirCOM.GetWavelengths(DeviceHandle, 0)
    activeWavelength = getWavelengths[0]
    print('(2) The wavelength is set to: ' + getWavelengths[1][activeWavelength] + 'nm')

    getRange = OphirCOM.GetRanges(DeviceHandle, 0)
    activeRange = getRange[0]
    print('(3) The active measuring range is: ' + getRange[1][activeRange])

    print('If the sensor calibration needs to be adjusted, refer to Daniel Luoma\n')

    return

def stop_pulsar():

    global OphirCOM
    
    # Stop & Close all devices
    OphirCOM.StopAllStreams()
    OphirCOM.CloseAll()
    # Release the object
    OphirCOM = None

    print('\nPulsar deactivated succesfully.')

    return

def read_pulsar():

    global pulsarReading

    data = OphirCOM.GetData(DeviceHandle, 0)
    if len(data[0]) > 0:		# if any data available, print the first one from the batch
        #print('Reading = {0}, TimeStamp = {1}, Status = {2} '.format(data[0][0] ,data[1][0] ,data[2][0]))
        pulsarReading = data[0][0]
     
    else:
        print('\nNo Sensor attached to {0} !!!'.format(Device))

    return

def write_file():

    global n_measurements
    global counts_prev
    global pulsarReading

    counts = counts_now - counts_prev
    n_measurements += 1

    sys.stdout.write('\r\033[K|Time: ' + '{:.2f}'.format(n_measurements * interval) + 's| ' + 
    '|Counts: ' + str(counts) + '| |Power: ' + str(pulsarReading) + '|')
    
    wrt_file.write(str(counts) + ',' + str(pulsarReading) + ',' +  str(n_measurements * interval) + '\n')

    return

def main():

    global counts_prev

    clear_screen()
    prepare_file()

    # NI-device
    start_ni_device()
    # Pulsar
    start_pulsar()

    print('To save data and exit the program hit: ctrl + c')
    print('=============================================')
    print('Measurement data:')

    while True :
        time.sleep(interval)
        read_pulsar()
        read_PMTcounts()
        
        if counts_prev != None:
            write_file()
        
        counts_prev = counts_now


if __name__ == '__main__':
    try:
         main()
    except KeyboardInterrupt: # This way the program can be used without threading.
        exit_program()