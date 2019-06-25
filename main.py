#!/usr/bin/python
import numpy as np;
import random;
import sys
import math

arglen = len(sys.argv)
chordsToWrite = 0;

print("# of arguments: "+str(arglen))
print(sys.argv[0])

read = False;

if arglen > 3 or arglen < 2:
    print("Need at least one argument")
    exit(1)

if sys.argv[1] == "read":
    read = True;

if arglen == 3:
    chordsToWrite = int(sys.argv[2]);

masterArray = np.ones(shape=(6,6))
frequencyArray = np.ones(shape=(6,1))

file = open("weights.db","r")
dataset = open("datasets.db","r")
frequencyFile = open("frequencies.db","r")
chords = "CDEFGA"
outputChords = [];
outputChordFile = open("written_chords.txt","w+");

def readWeights():
    global masterArray
    i=0
    for line in file:
        currentSplit = line.split()
        for j in range(0,6):
            masterArray[i][j] = float(currentSplit[0])
        i = i + 1

def writeWeights():
    file = open("weights.db","w")
    for i in range(0, 6):
        for j in range(0,6):
            file.write(str(masterArray.tolist()[i][j]) + " ")
        file.write("\n")

    file.close()

def readFrequencies():
    global frequencyArray
    i = 0
    for line in frequencyFile:
        frequencyArray[i][0] = float(line)
    i += 1

def writeFrequencies():
    frequencyFile = open("frequencies.db","w")
    for i in range(0, 6):
        frequencyFile.write(str(frequencyArray[i][0]) + "\n")
    frequencyFile.close()


def initializeWeights():
    global masterArray
    masterArray = np.random.rand(6,6)
    normalizeRows(masterArray)
    file = open("weights.db","w")
    for i in range(0, 6):
        for j in range(0,6):
            file.write(str(masterArray.tolist()[i][j]) + " ")
        file.write("\n")

    file.close()


def normalizeRows (arr):
    rowSums = np.sum(a = arr,axis = 1)
    for i in range(0,6):
        arr[i] *= float(1) / float(rowSums[i]);
        #print(float(1) / float(rowSums[i]))

def normalizeCols (arr):
    colSums = np.sum(a = arr, axis = 0)
    for i in range(0, 6):
        arr[i] *= float(1) / float(colSums)

def updateWeight(str):
    for i in range(0,4):
        currentChord = str[i]
        nextChord = str[i + 1 if i < 3 else 0]
        currentChordRow = chords.index(currentChord)
        nextChordCol = chords.index(nextChord)
        masterArray[currentChordRow][nextChordCol] += 0.05
    normalizeRows(masterArray)

def updateAllWeights():
    for line in dataset:
        updateWeight(line)

def updateFrequency(str):
    occurrences = []
    for i in range(0, 6):
        occurrences.append(0)
    for i in range(0, 4):
        currentChord = str[i]
        currentChordRow = chords.index(currentChord)
        occurrences[currentChordRow] += 1
        if occurrences[currentChordRow] > 1:
            frequencyArray[currentChordRow] += 0.05;


def updateAllFrequencies():
    print("Updating all frequencies: ")
    dataset = open("datasets.db","r")
    for line in dataset:
        updateFrequency(line)
    normalizeCols(frequencyArray)

def decideNextChord(i, chords):
    distribution = np.empty(7, dtype=float)

    distribution[0] = 0.0;

    occurrencesInChord = []
    for i in range(0, 6):
        occurrencesInChord.append(0)

    lastCut = 0.0;
    for j in range(0,6):
        gap = masterArray[i][j];
        for c in chords:
            if c == j:
                #gap *= 0.5 + frequencyArray[j];
                #gap *= (5 - occurrencesInChord[j])/5
                occurrencesInChord[j] += 1
        lastCut += (gap + frequencyArray[j]) * (5 - occurrencesInChord[j]) / 5;
        distribution[j + 1] = lastCut;

    #distribution = [float(i)/sum(distribution) for i in distribution]
    print(distribution)
    print(distribution[6])
    choice=random.random() * distribution[6]

    for j in range(0,6):
        lowerBound = distribution[j]
        topBound = distribution[j + 1]
        if lowerBound <= choice and choice < topBound:
            return j

    return -1

def pickNewChordIndex():
    global frequencyArray
    distribution = []
    distribution.append(0.0)

    lastCut = 0.0

    for i in range(0, 6):
        gap = frequencyArray[i][0]
        lastCut += gap
        distribution.append(lastCut)

    print("First chord distribution")
    print(distribution)

    choice=random.random() * distribution[6]

    for j in range(0,6):
        lowerBound = distribution[j]
        topBound = distribution[j + 1]
        if lowerBound <= choice and choice < topBound:
            return j
    return 5

def considerFrequencies():
    global masterArray
    global frequencyArray
    for i in range(0, 6):
            print()


if read:
    readWeights()
    readFrequencies()
else:
    initializeWeights()


updateAllWeights()
updateAllFrequencies()



if arglen > 2:
    chordIndex = pickNewChordIndex()
    outputChords.append(chordIndex);
    for i in range(1, chordsToWrite):
        chordIndex = decideNextChord(chordIndex, outputChords)
        outputChords.append(chordIndex)

for i in outputChords:
    print(chords[i])

for i in outputChords:
    outputChordFile.write(chords[i] + "\n")

writeWeights()
writeFrequencies()
