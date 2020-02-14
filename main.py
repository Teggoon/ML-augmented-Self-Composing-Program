#!/usr/bin/python
import numpy as np;
import random;
import sys
import math

# Line 7 to 25 just processes user input; 
# If "read" isn't given, then the program initializes the weights used to pick chords. 
# If "read" is    given, then the program simply reads from the weights.db file.
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
    
 

# masterArray stores the probability of each chord.
masterArray = np.ones(shape=(6,6))

# frequencyArray stores the frequency of each chord.
frequencyArray = np.ones(shape=(6,1))

# Basic global variables
file = open("weights.db","r")
dataset = open("datasets.db","r")
frequencyFile = open("frequencies.db","r")
chords = "CDEFGA"
outputChords = [];
outputChordFile = open("written_chords.txt","w+");

#populating masterArray with weights from the weights file
def readWeights():
    global masterArray
    i=0
    for line in file:
        currentSplit = line.split()
        for j in range(0,6):
            masterArray[i][j] = float(currentSplit[0])
        i = i + 1

# Writing to the weights file with new information
def writeWeights():
    file = open("weights.db","w")
    for i in range(0, 6):
        for j in range(0,6):
            file.write(str(masterArray.tolist()[i][j]) + " ")
        file.write("\n")

    file.close()

# populating the frequency array with the frequency file's values.
def readFrequencies():
    global frequencyArray
    i = 0
    for line in frequencyFile:
        frequencyArray[i][0] = float(line)
    i += 1

# Writing to the frequency file with new information
def writeFrequencies():
    frequencyFile = open("frequencies.db","w")
    for i in range(0, 6):
        frequencyFile.write(str(frequencyArray[i][0]) + "\n")
    frequencyFile.close()

# Initialize weights if there were no weights.db set up.
# This writes to a new file, weights.db
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

# Flattening out the rows of any given matrix to it.
def normalizeRows (arr):
    rowSums = np.sum(a = arr,axis = 1)
    for i in range(0,6):
        arr[i] *= float(1) / float(rowSums[i]);
        #print(float(1) / float(rowSums[i]))

# Flattening out the columns of any given matrix to it
def normalizeCols (arr):
    colSums = np.sum(a = arr, axis = 0)
    for i in range(0, 6):
        arr[i] *= float(1) / float(colSums)

# Updating masterArray's weights given a chord-progression input.
# the input is a string like "CFGA", where each letter is a chord.
def updateWeight(str):
    for i in range(0,4):
        currentChord = str[i]
        nextChord = str[i + 1 if i < 3 else 0]
        currentChordRow = chords.index(currentChord)
        nextChordCol = chords.index(nextChord)
        masterArray[currentChordRow][nextChordCol] += 0.05
    normalizeRows(masterArray)

# Collective updating all weights based on raw chord prog data
def updateAllWeights():
    for line in dataset:
        updateWeight(line)

# Updating the frequency array with input string of chord progressions
# str is a string like "AFCG", where each letter is a chord.
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

# collectively updating frequencies based on raw chord prog data
def updateAllFrequencies():
    print("Updating all frequencies: ")
    dataset = open("datasets.db","r")
    for line in dataset:
        updateFrequency(line)
    normalizeCols(frequencyArray)

# Function that decides next chord to choose base on current chord
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

# Picking the new first chord
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



# Actually calling all the functions now

if read:
    readWeights()
    readFrequencies()
else:
    initializeWeights()


updateAllWeights()
updateAllFrequencies()


# Basic code handling the creation of a new chord progression
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
