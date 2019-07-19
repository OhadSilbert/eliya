import asyncio
import serial_asyncio
import matplotlib.pyplot as plt
from collections import deque
import struct
import serial


class Output(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self.transport = None
        self.history = deque(maxlen=100)
        self.buf = b''
        self.start_read = False
        self.start_buf = b''
        plt.axis([0, 100, 0, 1025])
        self.last_emg_sig = 0

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False
        self.start_read = False
        self.last_emg_sig = 0

    def data_received(self, data):
        for i in range(len(data)):
            bdata = data[i:i+1]
            if self.start_read:
                self.buf += bdata
            else:
                self.start_buf += bdata
                if len(self.start_buf) >= 2:
                    esc = struct.unpack('!H', self.start_buf[-2:])[0]
                    if esc == 65535:
                        self.start_buf = b''
                        self.start_read = True

            if len(self.buf) == 2:
                emg_sig = struct.unpack('!H', self.buf[::-1])[0]
                if emg_sig - self.last_emg_sig != 10:
                    print(emg_sig)
                self.last_emg_sig = emg_sig
                self.history.append(emg_sig)
                self.buf = b''
                self.start_read = False

                if len(self.history) == 100:
                    plt.clf()
                plt.axis([0, 100, 0, 1025])
                plt.plot(list(range(len(self.history))), list(self.history), 'g-')
                plt.pause(0.01)
            elif len(self.buf) > 2:
                print('ERROR')
        # self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()
        plt.show()


def main():
    loop = asyncio.get_event_loop()
    coro = serial_asyncio.create_serial_connection(loop, Output, 'COM3', baudrate=9600)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
    # arduino = serial.serial_for_url('COM3', baudrate=9600, timeout=.1)
    # last_data = 5
    # while True:
    #     data = arduino.readline()[:-2]  # the last bit gets rid of the new-line chars
    #     if data:
    #         new_data = int(data)
    #         if new_data - last_data != 1:
    #             print(new_data)
    #         last_data = new_data



if __name__ == '__main__':
    main()
