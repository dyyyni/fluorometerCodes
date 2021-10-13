############################################################################################################
# This algorithm finds signals from real-time streams. 
# The algorithm is based on statistical dispersion
# - If a new datapoint is a given x number of standard deviations away of some moving mean
#   --> The algorithm initiates a signal
# - The signal can either be 1 for a positive signal or (-1) for a negative signal
# - The signals will be read as e.g. 01(-1)00110(-1)01 etc.
#
# Key concepts to understand how the algorithm works: lag, threshold and influence
#
# Lag :  the lag parameter determines how much your data will be smoothed and how adaptive the algorithm
# is to changes in the long-term average of the data
#
# Influence : this parameter determines the influence of signals on the algorithm's detection threshold.
#
# Threshold :  the threshold parameter is the number of standard deviations from the moving mean above which
# the algorithm will classify a new datapoint as being a signal.
#
# Brakel, J.P.G. van (2014). "Robust peak detection algorithm using z-scores". Stack Overflow. Available at: 
# https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/22640362#22640362
# (version: 2020-11-08).
#
# Modified to be used in the project Optonome by
# Daniel Luoma (11.10.2021)
#
# To do :
# 1. Comment the class so that it can be understood by you (and maybe by someone else) []
# - Modifications for the code in order to make it usable in Optonome
# 2. Ponder if the negative signal is of any use []
#  - Maybe I want the signals array/negative signals as the return, could be interesting to see how the water behaves
# 3. Do I need this to be a threaded action in the actual running code? []
# 4. if so how to make it like that? Read about python threading.
############################################################################################################

import numpy as np

class real_time_peak_detection():
    # Class initiation function - this is to be used as the object is first created
    def __init__(self, array, lag, threshold, influence):
        self.y = list(array) # Provide an array which has the updating data in it
        self.length = len(self.y)
        self.lag = lag # Can be thought as how much data we let in before we estimate the mean
        self.threshold = threshold
        self.influence = influence
        self.signals = [0] * len(self.y) # initially there is 0 signals
        self.filteredY = np.array(self.y).tolist()
        self.avgFilter = [0] * len(self.y)
        self.stdFilter = [0] * len(self.y)

    # This function is used to feed new data to the algorithm. Call this function inside the for-loop for data read
    # Returns the signals array from the class-object (updated signal will be a 1 or -1, 0 will be used for no signal in the array)
    def thresholding_algo(self, new_value):
        self.y.append(new_value) # Adds the new value to the evergrowing list of datapoints
        i = len(self.y) - 1
        self.length = len(self.y)
        if i < self.lag:
            return 0
        elif i == self.lag:
            self.signals = [0] * len(self.y)
            self.filteredY = np.array(self.y).tolist()
            self.avgFilter = [0] * len(self.y)
            self.stdFilter = [0] * len(self.y)
            self.avgFilter[self.lag] = np.mean(self.y[0:self.lag]).tolist()
            self.stdFilter[self.lag] = np.std(self.y[0:self.lag]).tolist()
            return 0

        self.signals += [0]
        self.filteredY += [0]
        self.avgFilter += [0]
        self.stdFilter += [0]
 
        if abs(self.y[i] - self.avgFilter[i - 1]) > self.threshold * self.stdFilter[i - 1]:
            if self.y[i] > self.avgFilter[i - 1]:
                self.signals[i] = 1 # positive signal
            else:
                self.signals[i] = -1 # negative signal <-- might need to remove/change this. 

            # Modifies the mean based on the influence given to the signals
            self.filteredY[i] = self.influence * self.y[i] + (1 - self.influence) * self.filteredY[i - 1]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])
        else:
            self.signals[i] = 0 # No signal to be found
            self.filteredY[i] = self.y[i]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])

        return self.signals[i]