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
tempo    = 400 + math.floor(random.random() * 100)   # In BPM
volume   = 100  # 0-127, as per the MIDI standard
key = -15 + math.floor(random.random() * 12)

volumePack = [60,60,60,60,60,60,60,60]

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

loop = 4

layerUp = math.floor(random.random() * 2)

arpeggioLayer = [0, 2, 1, 0, 2, 1, 0, 1]

for n in range(0, loop):
    for c, i in enumerate(chords):
        currentChord = chords[c];
        for v in range(0, len(volumePack)):
            if arpeggioLayer[v] == 1:
                MyMIDI.addNote(track, channel, key + chordsReference[currentChord][1] + 12, time + c*8 + v + n * 32, duration, volumePack[v])
            else:
                MyMIDI.addNote(track, channel, key + chordsReference[currentChord][arpeggioLayer[v]], time + c*8 + v + n * 32, duration, volumePack[v])



def printToMIDI():
    with open("generated_chords.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

printToMIDI()
