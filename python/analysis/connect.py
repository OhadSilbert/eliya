import matplotlib.pyplot as plt
import numpy as np
from threading import Thread, Event
from collections import deque
from queue import Queue
import serial
import time


class SerialTextRead(Thread):
    def __init__(self, url='COM3'):
        super().__init__()
        self._queue = Queue()
        # self._arduino = serial.serial_for_url(url, baudrate=9600, timeout=.1)
        self.timeout = -1
        self._stop_event = Event()

    def get_queue(self):
        return self._queue

    def stop(self):
        self._stop_event.set()

    def run(self):
        start_time = time.time()
        current_time = time.time() - start_time
        while not self._stop_event.is_set() and (self.timeout < 0 or current_time < self.timeout):
            current_time = time.time() - start_time
            data = b'100\n\r'#self._arduino.readline()
            if len(data) > 2:
                emg_sig = int(data[:-2])  # the last bit gets rid of the new-line chars
                data_point = (current_time, emg_sig)
                self._queue.put(data_point)
                pass
            pass
        pass

    def loop(self, timeout=-1):
        self.timeout = timeout
        self.start()


def live_plotter(x_vec, y1_data, line1, identifier='', pause_time=0.1, time_window=20):
    if line1 == []:
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, '-', alpha=0.8)
        plt.ylabel('EMG Signal')
        plt.xlabel('time [sec]')
        plt.title(identifier)
        plt.axis([-time_window, 0, 0, 1025])
        plt.show()

    line1.set_xdata(x_vec)
    line1.set_ydata(y1_data)

    plt.xlim([x_vec[-1] - time_window, x_vec[-1]])

    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1


def main():
    timeout = 20
    time_window = 10
    serieal = SerialTextRead(url='COM3')
    serieal.loop()
    size = time_window * 100
    q = deque(maxlen=size)
    for _ in range(size):
        q.append((0., 0.))
    line1 = []
    start_time = time.time()
    current_time = time.time() - start_time
    aa = []
    while timeout < 0 or current_time < timeout:
        current_time = time.time() - start_time
        while not serieal.get_queue().empty():
            q.append(serieal.get_queue().get())
            aa += [q]

    x_vec, y_vec = zip(*q)
    line1 = live_plotter(list(x_vec), list(y_vec), line1, time_window=time_window, identifier='EMG')
    serieal.stop()
    serieal.join()


if __name__ == '__main__':
    # main()
    import sounddevice as sd

    fs = 44100
    data = np.random.uniform(-1, 1, fs)
    for i in range(1000):
        r = np.random.randint(2,15)
        time.sleep(r)
        print(f'now {r}')
        sd.play(data, fs, blocking=True)




    # from playsound import playsound
    # playsound('audio.mp3')