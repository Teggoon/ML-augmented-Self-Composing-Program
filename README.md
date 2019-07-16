# Music Theory based Self-Composing Program

A program that composes EDM chords and arpeggio melodies based on learned weights from datasets of chord progressions.

During the learning phase, the program takes in datasets of popular four-chord EDM harmonic progressions and populate two matrices: one that calculates each chord's likelihood to follow another chord, one that calculates the popularity of chords (how much a chord is usually repeated within a chord progression).

The chord-composing process makes use of a Markov chain structure. For each chord chosen, the program first calculates a normalized distribution based on data from the first matrix. The program also takes into account the chords already used, meaning chords that are used would have their likelihood of being chosen lowered (although that's where the 2nd matrix comes into play: chords that are often repeated in real life EDM are still more likely to be selected).
