#!/usr/bin/python

from midiutil import MIDIFile
import math
import random

chordsReference = {
    "C": (60, 64, 67),
    "D": (62, 65, 69),
    "E": (64, 67, 71),
    "F": (65, 69, 72),
    "G": (67, 71, 74),
    "A": (69, 72, 76),
}


file = open("written_chords.txt","r")

chords = []

for line in file:
    chords.append(line[0])

degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 400   # In BPM
volume   = 100  # 0-127, as per the MIDI standard
key = -6 + math.floor(random.random() * 12)

volumePack = [60,30,40,80,40,60,90]

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

loop = 4

for n in range(0, loop):
    for c, i in enumerate(chords):
        currentChord = chords[c];
        for v in range(0, len(volumePack)):
            for j in range(0,3):
                MyMIDI.addNote(track, channel, key + chordsReference[currentChord][j], time + c*8 + v + n * 32, duration, volumePack[v])


with open("generated_chords.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
