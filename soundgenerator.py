import numpy as np
import sounddevice as sd
import time

"""
A small music player for writing chord notations.
2022-07-09: Vesa Koiramäki - Project started
"""

class Tune:

    def __init__(self, samplerate = 44100):
        self.samplerate = 44100
        sd.default.samplerate = samplerate
        self.amp = 0.25

    noteNotations = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

    pauses = {
        "_": (0.00,)
    }

    notes = {

        "A": 440.00,
        "A#": 466.16, 
        "B": 493.88,
        "C" : 523.25,
        "C#" : 554.37,
        "D" : 587.37,
        "D#" : 622.25,
        "E" : 659.25,
        "F" : 698.46,
        "F#" : 739.99,
        "G" : 783.99,
        "G#" : 830.61,
        
    }

    chords = {

    }

    for idx, keyNote in enumerate(noteNotations):

        nTones = len(noteNotations)
        minScale = 1
        majScale = 1
        dimScale = 1
        scale = 1

        if((idx + 3) > len(noteNotations)):
            minScale = 2

        if((idx + 4) > len(noteNotations)):
            majScale = 2

        if((idx + 6) > len(noteNotations)):
            dimScale = 2
        
        if((idx + 7) > len(noteNotations)):
            scale = 2

        chords[keyNote] = (notes[noteNotations[idx]],)
        chords[keyNote + "min"] = notes[noteNotations[idx]], notes[noteNotations[(idx + 3)%nTones]] * minScale, notes[noteNotations[(idx+7)%nTones]] * scale
        chords[keyNote + "maj"] = notes[noteNotations[idx]], notes[noteNotations[(idx + 4)%nTones]] * majScale, notes[noteNotations[(idx+7)%nTones]] * scale
        chords[keyNote + "dim"] = notes[noteNotations[idx]], notes[noteNotations[(idx + 3)%nTones]] * minScale, notes[noteNotations[(idx+6)%nTones]] * dimScale

    keys = {}
    keys.update(chords)
    keys.update(pauses)

    print(keys)

    def playKey(self, keyword, duration):

        t = np.arange(np.ceil(duration * self.samplerate)) / self.samplerate

        freqs = self.keys[keyword]

        signal = self.amp * np.ceil(0 * t)

        for freq in freqs:

            signal += self.amp * np.sin(2.0 * np.pi * freq * t)

        sd.play(signal)
        time.sleep(duration)


