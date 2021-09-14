#!/usr/bin/env python3

import random as rnd
import sys, time, re


pureNotes = ['C or B\u266F', 'C\u266F or D\u266D', 'D', 'D\u266F or E\u266D', 'E or F\u266D', 'F or E\u266F', 'F\u266F or G\u266D', 'G', 'G\u266F or A\u266D', 'A', 'A\u266F or B\u266D', 'B or C\u266D']

# define major notes
majors = ['C Major', 'D Major', 'E Major', 'F Major', 'G Major', 'A Major', 'B Major']

# define minor notes
minors = ['C Minor', 'D Minor', 'E Minor', 'F Minor', 'G Minor', 'A Minor', 'B Minor']

# define accidentals
sharps = []
flats = []
accidental = ['\u266F', '\u266D'] # sharp and flat characters

for y in accidental:
    if y == '\u266F':
        for x in majors:
            note = x.split()
            sharps.append((f"{note[0]}{accidental[0]} {note[1]}"))
        for x in minors:
            note = x.split()
            sharps.append((f"{note[0]}{accidental[0]} {note[1]}"))
    elif y == '\u266D':
        for x in majors:
            note = x.split()
            flats.append(f"{note[0]}{accidental[1]} {note[1]}")
        for x in minors:
            note = x.split()
            flats.append(f"{note[0]}{accidental[1]} {note[1]}")
accidentals = sharps + flats
allNotes = accidentals + majors + minors

# Should rewrite this function in a way so numbers and lists for options are updated automatically
# if more options are added to 'askDiff' input
def difficulty(askDiff):
    notes = []
    if "1" in askDiff:
        notes += majors
    if "2" in askDiff:
        notes += minors
    if "3" in askDiff:
        notes += sharps
    if "4" in askDiff:
        notes += flats
    if "5" in askDiff:
        notes = allNotes

    emptyInput = 0
    for x in ['1', '2', '3', '4', '5']:
        if x not in askDiff:
            emptyInput += 1
            if emptyInput > 4:
                return None
    rnd.shuffle(notes)
    return notes


def askQuestion(notes):
    rndTone = rnd.randint(2, 7)
    numSuffix = ""
    rndNote = notes[rnd.randint(0, len(notes)-1)]
    if rndTone == 1:
        numSuffix = "st"
        quest = (f"What is the {rndTone}{numSuffix} tone of {rndNote}?")
        print(quest)
        return rndTone, rndNote.split()
    elif rndTone == 2:
        numSuffix = "nd"
        quest = (f"What is the {rndTone}{numSuffix} tone of {rndNote}?")
        print(quest)
        return rndTone, rndNote.split()
    elif rndTone == 3:
        numSuffix = "rd"
        quest = (f"What is the {rndTone}{numSuffix} tone of {rndNote}?")
        print(quest)
        return rndTone, rndNote.split()
    else:
        numSuffix = "th"
        quest = (f"What is the {rndTone}{numSuffix} tone of {rndNote}?")
        print(quest)
        return rndTone, rndNote.split()

# -- This block off code contains all processes that are involved in finding the answer --

def findNote(note):
    notePlace = 0
    for x in pureNotes:     
        noteRex = re.search(rf"(^|[ ])({note})([ ]|$)", x)
        if noteRex:
            return notePlace
        else:
            notePlace += 1

def findTone(tone, notePlace, majOrMin):
    if majOrMin == 'Major':
        scaleFormula = 'WWHWWWH'
        scaleSteps = scaleFormula[0:tone-1]
        toneAns = str()        
        for x in scaleSteps:
            restartListW = (notePlace+2) - (len(pureNotes))
            restartListH = (notePlace+1) - (len(pureNotes))
            if x == 'W':
                if restartListW > 0:
                    notePlace = 0
                    notePlace += restartListW
                    toneAns = pureNotes[notePlace]
                elif restartListW == 0:
                    notePlace = 0
                    toneAns = pureNotes[notePlace]
                else:
                    notePlace+=2
                    toneAns = pureNotes[notePlace]
            if x == 'H':
                if restartListH > 0:
                    notePlace = 0
                    notePlace += 1
                    toneAns = pureNotes[notePlace]
                elif restartListH == 0:
                    notePlace = 0
                    toneAns = pureNotes[notePlace]
                else:
                    notePlace += 1
                    toneAns = pureNotes[notePlace]
        return toneAns
    elif majOrMin == 'Minor':
        scaleFormula = 'WHWWHWW'
        scaleSteps = scaleFormula[0:tone-1]
        toneAns = str()
        for x in scaleSteps:
            restartListW = (notePlace+2) - (len(pureNotes))
            restartListH = (notePlace+1) - (len(pureNotes))
            if x == 'W':
                if restartListW > 0:
                    notePlace = 0
                    notePlace += restartListW
                    toneAns = pureNotes[notePlace]
                elif restartListW == 0:
                    notePlace = 0
                    toneAns = pureNotes[notePlace]
                else:
                    notePlace+=2
                    toneAns = pureNotes[notePlace]
            if x == 'H':
                if restartListH > 0:
                    notePlace = 0
                    notePlace += 1
                    toneAns = pureNotes[notePlace]
                elif restartListH == 0:
                    notePlace = 0
                    toneAns = pureNotes[notePlace]
                else:
                    notePlace += 1
                    toneAns = pureNotes[notePlace]
        return toneAns

def findAnswer(note, tone, majOrMin):
    notePlace = findNote(note)
    toneAns = findTone(tone, notePlace, majOrMin)
    return toneAns

def giveAnswer(question):
    tone = question[0]
    note = question[1][0]
    majOrMin = question[1][1]
    answer = findAnswer(note, tone, majOrMin)
    print(f"* Answer: {answer}\n")
    return answer

# ---------------- Answer Found ------------------

if len(sys.argv) > 1:
    askDiff = sys.argv[1]
else:
    askDiff = input("""
    ----------------------------------------\n
            Select the difficulty:

        1 - Include major scales
        2 - Include minor scales
        3 - Include sharp accidentals (\u266F)
        4 - Include flat accidentals (\u266D)
        5 - Include all of the above

        Include: """)
    print("""\n----------------------------------------\n""")

if difficulty(askDiff) != None :
    level = difficulty(askDiff)
    print("Let's begin:")
    print('(Press "enter" to reveal the answer or type "exit" to quit)\n')
    while True:
        try:
            time.sleep(0.5)
            question = askQuestion(level)
            pauseInput = input("")
            giveAnswer(question)
        except:
            print("\nGoodbye\n")
            sys.exit()
