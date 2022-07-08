import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import time

"""
Produces simple chord progression for minor and major scales by key.
8-JUN-2022 / Vesa Koiramäki
"""

minorScale = [0, 2, 1, 2, 2, 1, 2, 2]
majorScale = [0, 2, 2, 1, 2, 2, 2, 1]

minorDegreeMajor = [False, False, True, False, False, True, True] 
majorDegreeMajor = [True, False, False, True, True, False, False] 


noteNotations = ["A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"]

"""
Note frequences
"""
notes = {}

for idx, note in enumerate(noteNotations):
    notes[note] = 440 + ((440 / len(noteNotations)) * idx)

print(notes)


"""
Chords
"""

chords = {

    "Amin": (notes["A"], notes["C"], notes["Ds"]),
    "Amaj": (notes["A"], notes["Cs"], notes["Ds"])
}

for idx, keyNote in enumerate(noteNotations):
    chords[keyNote + "min"] = notes[noteNotations[idx%len(noteNotations)]], notes[noteNotations[(idx + 3)%len(noteNotations)]], notes[noteNotations[(idx+7)%len(noteNotations)]]
    chords[keyNote + "maj"] = notes[noteNotations[idx%len(noteNotations)]], notes[noteNotations[(idx + 4)%len(noteNotations)]], notes[noteNotations[(idx+7)%len(noteNotations)]]

print(chords)

key = None
while(key not in noteNotations):
    key = input(f"Please give key for chord progression ({noteNotations}): ")

print(key)

scaleType = None
while(scaleType not in ["M", "m"]):
    scaleType = input("Do you want the progression to be major (M) or minor (m) scale? [M/m]: ")


scale = []
print(key)
idx = noteNotations.index(key)
if(scaleType == "M"):
    for progressionStep in majorScale:
        idx = idx + progressionStep
        note = noteNotations[idx%len(noteNotations)]
        scale.append(notes[note])
        degreeMajor = majorDegreeMajor
elif(scaleType == "m"):
    for progressionStep in minorScale:
        idx = idx + progressionStep
        note = noteNotations[idx%len(noteNotations)]
        scale.append(notes[note])
        degreeMajor = minorDegreeMajor

chordProgression = []
for idx, freq in enumerate(scale[0:7]):
    noteF = None
    for note, value in notes.items():
        if(freq == value):
            noteF = note
    if(degreeMajor[idx]):
        chordProgression.append(noteF + "maj")
    else:
        chordProgression.append(noteF + "min")

print(chordProgression)


samplerate = 44100
dur = 1
amp = 0.15
t = np.arange(np.ceil(dur * samplerate)) / samplerate
print(t)

progression = input("Insert a serie of digits between 1 to 7 separated by comma, i.e. 1, 7, 6, 7: ")
progression = progression.strip().split(",")

for number in progression:
    print(progression, number)
    chord = chordProgression[int(number)-1]
    print(chord)
    freq = chords[chord]
    print(freq)
    signal1 = amp * np.sin(2.0 * np.pi * freq[0] * t)
    signal2 = amp * np.sin(2.0 * np.pi * freq[1] * t)
    signal3 = amp * np.sin(2.0 * np.pi * freq[2] * t)

    signal = signal1 + signal2 + signal3

#print(signal)

    plt.plot(signal1[:int(samplerate/freq[0])])
    plt.plot(signal2[:int(samplerate/freq[1])])
    plt.plot(signal3[:int(samplerate/freq[2])])
    plt.plot(signal[:int(samplerate/freq[0])])
    plt.show()

    sd.play(signal, samplerate)
    time.sleep(dur)
