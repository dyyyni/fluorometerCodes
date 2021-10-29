import os
import sys
import time

# self-made modules
import niMXControl
import spikeDetection

niDevice = niMXControl.NIControl()

def clear_screen():

    os.system('cls')

    return

def exit_program():
    # Used to safely deactivate the ni device 
    print('\n*********************************************')
    print('Exiting Program..\n')

    if niDevice.isNi: niDevice.stopNIDev()

    print('\nProgram Finished.')
    print('*********************************************')

    sys.exit(1)

def consoleLog(n_measurements, counts, interval, signal):
    sys.stdout.write('\r\033[K|Time: ' + '{:.2f}'.format(n_measurements * interval) + 's| ' + 
    '|Counts: ' + str(counts)+ '| signal: ' + str(signal))

    return

def main():

    # Detection algorithm initalisation
    data = []
    detector = spikeDetection.real_time_peak_detection(data, 60, 10, 0)

    clear_screen()
    niDevice.startNIDev()

    if niDevice.isNi == False: exit_program()

    interval = niDevice.sendInterval()

    print('To save data and exit the program hit: ctrl + c')
    print('=============================================')
    print('Measurement data:')

    while True:
        time.sleep(interval)
        niDevice.readCounts()

        if niDevice.send_countsPrev() != None:
            counts = niDevice.counts()
            signal = detector.thresholding_algo(counts)
            consoleLog(niDevice.send_n_measurements(), counts, interval, signal)
            

        niDevice.setPrevcounts()
    

if __name__ == '__main__':
    try:
         main()
    except KeyboardInterrupt: # This way the program can be used without threading.
        exit_program()