import matplotlib.pyplot as plt
import numpy as np
from threading import Thread, Event
from collections import deque
from queue import Queue
import serial
import time
import os
from datetime import datetime
import winsound
import random


class SerialTextRead(Thread):
    def __init__(self, url='COM3'):
        super().__init__()
        self._queue = Queue()
        self._arduino = serial.serial_for_url(url, baudrate=9600, timeout=.1)
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
            data = self._arduino.readline()
            data = data.decode("utf-8")
            fields = data.strip().split(',')
            if len(fields) == 2:
                emg_rectified_sig, emg_raw_sig = map(lambda x: float(x), fields)
                data_point = (current_time, emg_rectified_sig, emg_raw_sig)
                self._queue.put(data_point)
                pass
            pass
        pass

    def loop(self, timeout=-1):
        self.timeout = timeout
        self.start()


def live_plotter(x_vec, y1_data, y2_data, line1, line2, identifier='', pause_time=0.1, time_window=20):
    if line1 == [] or line2 == []:
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, '-g', alpha=0.8)
        line2, = ax.plot(x_vec, y2_data, '-r', alpha=0.8)
        plt.ylabel('EMG Signal')
        plt.xlabel('time [sec]')
        plt.title(identifier)
        plt.axis([-time_window, 0, 0, 1025])
        plt.show()

    line1.set_xdata(x_vec)
    line1.set_ydata(y1_data)
    line2.set_xdata(x_vec)
    line2.set_ydata(y2_data)

    plt.xlim([x_vec[-1] - time_window, x_vec[-1]])

    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1, line2


def get_dir_name():
    return os.path.dirname(__file__)


def get_file_name():
    return str(datetime.now()).replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_') + '.txt'


def beep():
    frequency = 500
    duration = 250
    winsound.Beep(frequency, duration)


def main():
    log_to_file = True
    do_beep = True
    timeout = -1
    time_window = 10
    number_of_points_per_second_from_arduion = 100  # defined in the arduino code
    beep_rate = 0.1  # beeps per second
    serieal = SerialTextRead(url='COM5')
    serieal.loop()
    size = time_window * number_of_points_per_second_from_arduion
    q = deque(maxlen=size)
    for _ in range(size):
        q.append((0., 0., 0.))
    line1 = []
    line2 = []
    start_time = time.time()
    current_time = time.time() - start_time
    file_name = os.path.join(get_dir_name(), get_file_name())
    while timeout < 0 or current_time < timeout:
        current_time = time.time() - start_time
        while not serieal.get_queue().empty():
            signal_value = serieal.get_queue().get()
            q.append(signal_value)
            mark = do_beep and (random.random() < (beep_rate / number_of_points_per_second_from_arduion))
            if mark:
                beep()
            if log_to_file:
                with open(file_name, 'a') as fout:
                    fout.write(f'{signal_value[0]},{signal_value[1]},{signal_value[2]},{int(mark)}\n')

        x_vec, y1_vec, y2_vec = zip(*q)
        line1, line2 = live_plotter(list(x_vec), list(y1_vec), list(y2_vec), line1, line2, time_window=time_window,
                                    identifier='EMG')
    serieal.stop()
    serieal.join()


if __name__ == '__main__':
    main()
