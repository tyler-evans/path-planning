import time


class Timer:

    def __init__(self):
        self.start_time = time.time()

    def end(self):
        self.elapsed_time = time.time() - self.start_time
