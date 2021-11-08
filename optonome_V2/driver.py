import os
import sys
import threading
import time

# self-made modules
import niMXControl
import spikeDetection

# Globals
niDevice = niMXControl.NIControl()
wrt_file = None

def clear_screen():

    os.system('cls')

    return

def prepare_file():

    global wrt_file

    fileName = input('Enter the filename: ')
    save_path = os.getcwd() + '\\' + fileName + '.csv'
    sys.stdout.write('Saving data to \'' + save_path + '\n\nInitialising...\n')

    wrt_file = open(save_path, 'w')
    wrt_file.write('sep=,\n')
    wrt_file.write('Counts(#/s), Signal(-1|0|1), Time(s)\n')

    return

def write_file(counts, signal, n_measurements, interval):

    global wrt_file
    
    wrt_file.write(str(counts) + ',' + str(signal) + ',' + str(n_measurements * interval) + '\n')

    return

def exit_program():

    global wrt_file
    global niDevice

    # Used to safely deactivate the ni device 
    print('\n*********************************************')
    print('Exiting Program..\n')

    if niDevice.isNi: niDevice.stopNIDev()
    if wrt_file != None : wrt_file.close()

    print('\nProgram Finished.')
    print('*********************************************')

    sys.exit(1)

def consoleLog(n_measurements, counts, interval, signal):
    sys.stdout.write('\r\033[K|Time: ' + '{:.2f}'.format(n_measurements * interval) + 's| ' + 
    '|Counts: ' + str(counts)+ '| signal: ' + str(signal))

    return

def solenoidControl():
    '''
    Controls the solenoid relay.
    '''
    global niDevice

    timeOpen = 5 # in seconds
    refractoryPeriod = 20 # in seconds

    niDevice.solenoid_ON()
    time.sleep(timeOpen)
    niDevice.solenoid_OFF()

    time.sleep(refractoryPeriod)

    return

def main():

    global wrt_file
    global niDevice

    # Detection algorithm initalisation
    data = []
    detector = spikeDetection.real_time_peak_detection(data, 60, 10, 0)

    clear_screen()
    niDevice.startNIDev()

    if niDevice.isNi == False: exit_program()

    prepare_file()

    interval = niDevice.sendInterval()

    print('To save data and exit the program hit: ctrl + c')
    print('=============================================')
    print('Measurement data:')

    solenoidThread = threading.Thread(target=solenoidControl)

    while True:
        time.sleep(interval)
        niDevice.readCounts()

        if niDevice.send_countsPrev() != None:
            n_measurements = niDevice.send_n_measurements()
            counts = niDevice.counts()
            signal = detector.thresholding_algo(counts)
            if signal == 1 and not solenoidThread.is_alive():
                try:
                    solenoidThread.start()
                except RuntimeError:
                    solenoidThread = threading.Thread(target=solenoidControl)
                    solenoidThread.start()
                
            consoleLog(n_measurements, counts, interval, signal)
            write_file(counts, signal, n_measurements, interval)
            

        niDevice.setPrevcounts()
    

if __name__ == '__main__':
    try:
         main()
    except KeyboardInterrupt: # This way the program can be used without threading.
        exit_program()