# globals
task = None
exit_flag = False
wrt_file = None
counts_prev = None
counts_now = None
interval = 1

n_measurements = 0


def clear_screen():
    import os

    os.system('cls')

    return


def set_interval():
    import sys

    global interval

    if sys.argv.__len__() < 2:
        return

    interval = float(sys.argv[1])

    return


def prepare_file():
    import os
    import sys

    global wrt_file

    save_path = os.getcwd() + '\\12hsadfTesti'
    sys.stdout.write('Saving data to \'' + save_path + '\'\nTo save data and exit the program hit Enter \nInitialising...')
    wrt_file = open(save_path, 'w')

    return


def start_device():
    import sys
    import nidaqmx as ni

    global task

    devices = ni.system.system.System.local().devices
    if devices.__len__() < 1:
        print('No NI device detected. Aborting program execution.')
        sys.exit(1)

    name = devices[0].name + '/ctr1'
    if devices.__len__() > 1:
        print('Multiple NI devices detected. Using device/channel \'' + name + '\'')

    task = ni.Task('digital readout')
    task.ci_channels.add_ci_count_edges_chan(name)
    task.start()

    return


def abort_acquisition():
    global exit_flag

    input()
    exit_flag = True

    return


def enable_user_input_abortion():
    import threading

    thread = threading.Thread(target=abort_acquisition)
    thread.start()

    return


def read_counts():
    import time

    global n_measurements
    global counts_now

    counts_now = task.ci_channels[0].ci_count
    time.sleep(interval)

    return


def write_counts():
    import sys
    import datetime

    global n_measurements
    global counts_prev

    counts = counts_now - counts_prev
    n_measurements += 1
    sys.stdout.write('\r\033[KCounts at ' + '{:.2f}'.format(n_measurements * interval) + 's: ' + str(counts))
    wrt_file.write(str(datetime.datetime.now()) + ' ' + str(counts) + '\n')

    return


def stop_device():
    task.stop()
    task.close()
    wrt_file.close()

    return


def main():

    global counts_prev

    clear_screen()
    set_interval()
    prepare_file()
    start_device()
    enable_user_input_abortion()

    while not exit_flag:
        read_counts()
        if counts_prev is not None:
            write_counts()

        counts_prev = counts_now

    stop_device()

    return


if __name__ == '__main__': main()