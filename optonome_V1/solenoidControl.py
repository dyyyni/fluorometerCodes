import nidaqmx as ni
import time

task = ni.Task()

def stop_ni_device():

    task.stop()
    task.close()

    print('NI device deactivated succesfully.')

    return

def main():
    task.do_channels.add_do_chan("Dev1/port1/line1")
    task.start()

    while True:
        task.write(True)
        time.sleep(2)
        task.write(False)
        time.sleep(2)



if __name__ == '__main__':
    try:
         main()
    except KeyboardInterrupt: # This way the program can be used without threading.
        stop_ni_device()