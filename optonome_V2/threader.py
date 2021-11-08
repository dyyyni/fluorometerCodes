import threading

class thread(threading.Thread):
    def __init__(self, thread_name, function):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.function = function
