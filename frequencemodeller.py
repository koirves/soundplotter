"""
Tool for plotting sound waves, 5.7.2022 / Vesa Koiramäki
"""

import sounddevice as sd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class waveGenerator():

    def __init__(self, sampleRate = 44100.0, freq = 210.0):

        self.sampleRate = sampleRate
        self.start_idx = 0
        self.freq = freq
        self.amplitude = 0.15

        self.data = []

    def playSine(self, outdata, frames, time, status):
    
        ptime = (np.arange(frames) + self.start_idx) / self.sampleRate
        ptime = ptime.reshape(-1, 1)

        outdata[:] = self.amplitude * np.sin(2.0 * np.pi * self.freq * ptime)

        self.start_idx += frames
        self.data += map(lambda x: (float(x[0]), float(x[1])),zip(outdata, ptime))

        print(f"Playing: {self.start_idx} {self.freq} {self.amplitude} {self.sampleRate}")

repeat = 250

for freq in [210, 420, 640, 840]:
    wg = waveGenerator(sampleRate=44100.0)
    wg.freq = freq
    with sd.OutputStream(callback=wg.playSine, channels=1):
        while(wg.start_idx < (wg.sampleRate/wg.freq)*repeat):
            print(f"Running: {wg.start_idx}")
            #continue

    plot = pd.DataFrame(wg.data, columns = ["Amplitude", "Time"])
    plot = plot.tail(int(wg.sampleRate/wg.freq)*3)
    print(plot)
    plot.plot(x = "Time", y = "Amplitude", xlabel = "Time (s)", ylabel="Amplitude", legend=False, title=f"Modelling frequence {freq} Hz")

plt.show()