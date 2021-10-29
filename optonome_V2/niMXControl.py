import nidaqmx as ni

class NIControl:

    def __init__(self):
        # is NI device attached to the computer
        self.isNi = False
        self.readTask = None
        self.solenoidTask = None
        
        # Data acquisition
        self.counts_prev = None
        self.counts_now = None
        self.n_measurements = 0
        self.interval = 1 # Measuring interval. Set to 1 measurement/second

    # DAQ-card setup and termination
    ###########################################################################################
    def startNIDev(self):
        """
        This function is set up to start the DAQ-card.
        Function checks if a NI-device is connected to the computer.
        You can see the name of your device in the NI-MAX software if it matters to you.
        """

        devices = ni.system.system.System.local().devices

        if devices.__len__() < 1:
            print('No NI device detected. Aborting program execution.')
            return
        else: self.isNi = True

        name = devices[0].name + '/ctr1'
        if devices.__len__() > 1:
            print('Multiple NI devices detected. Using device/channel \'' + name + '\'')

        if devices.__len__() == 1:
            print('NI device detected. Using device/channel \'' + name + '\'')

        # PMT to daq card connection
        self.readTask = ni.Task('digital readout')
        self.readTask.ci_channels.add_ci_count_edges_chan(name)
        self.readTask.start()
        
        # Solenoid relay to daq card connection
        self.solenoidTask = ni.Task()
        self.solenoidTask.do_channels.add_do_chan("Dev1/port1/line1")
        self.solenoidTask.start()

        return

    def stopNIDev(self):
        # Stops the NI tasks and closes the connection to the DAQ-card
        self.readTask.stop()
        self.readTask.close()

        self.solenoidTask.stop()
        self.solenoidTask.close()

        print('NI device deactivated succesfully.')

        return

    def isNi(self):
        return self.isNi

    ###########################################################################################

    # PMT readings
    ###########################################################################################
    def readCounts(self):
        # reads the PMT counts
        self.counts_now = self.readTask.ci_channels[0].ci_count

        return

    def counts(self):
        counts = self.counts_now - self.counts_prev
        self.n_measurements += 1

        return counts

    def sendInterval(self):
        return self.interval

    def send_n_measurements(self):
        return self.n_measurements

    def send_countsPrev(self):
        return self.counts_prev

    def setPrevcounts(self):
        self.counts_prev = self.counts_now
        return

    ###########################################################################################

    # Solenoid control
    ###########################################################################################
    def solenoid_ON(self):
        self.solenoidTask.write(True)
        return

    def solenoid_OFF(self):
        self.solenoidTask.write(False)
        return
    ###########################################################################################
