#!/usr/bin/python

from midiutil import MIDIFile
import math
import random

#the corresponding pitches for each chord
chordsReference = {
    "C": (60, 64, 67),
    "D": (62, 65, 69),
    "E": (64, 67, 71),
    "F": (65, 69, 72),
    "G": (67, 71, 74),
    "A": (69, 72, 76),
}


#written_chords.txt already contains the chords that were written by the machine
file = open("written_chords.txt","r")

chords = []

#populating chords array with written chords
for line in file:
    chords.append(line[0])

#The pitches of the notes in the octave
degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 400 + math.floor(random.random() * 100)   # In BPM
volume   = 100  # 0-127, as per the MIDI standard
key = -15 + math.floor(random.random() * 12)

# Option to create dynamics in the arpeggio
volumePack = [60,60,60,60,60,60,60,60]

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

#How many times we want the arp loop to run
loop = 4

#Randomize how many octaves up we want to shift our arps
layerUp = math.floor(random.random() * 2)

#Actual design of the arp; this isn't randomized or written by machine, but designed manually.
arpeggioLayer = [0, 2, 1, 0, 2, 1, 0, 1]

#For each chord loop:
for n in range(0, loop):
    #for each chord:
    for c, i in enumerate(chords):
        
        #get current chord
        currentChord = chords[c];
        
        #Write out each note
        for v in range(0, len(volumePack)):
            if arpeggioLayer[v] == 1:
                MyMIDI.addNote(track, channel, key + chordsReference[currentChord][1] + 12, time + c*8 + v + n * 32, duration, volumePack[v])
            else:
                MyMIDI.addNote(track, channel, key + chordsReference[currentChord][arpeggioLayer[v]], time + c*8 + v + n * 32, duration, volumePack[v])


#Export to MIDI
def printToMIDI():
    with open("generated_chords.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

printToMIDI()
