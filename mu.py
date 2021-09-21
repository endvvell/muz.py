#!/usr/bin/env python3

import random as rnd
import sys, re

natural = b'\xe2\x99\xae'.decode('utf-8')
sharp = b'\xe2\x99\xaf'.decode('utf-8')
flat = b'\xe2\x99\xad'.decode('utf-8')
dSharp = b'\xf0\x9d\x84\xaa'.decode('utf-8')
dFlat = b'\xf0\x9d\x84\xab'.decode('utf-8')

accidentalType = [natural, sharp, flat, dSharp, dFlat]

octave = {
    'C' : [f'B{sharp}', f'D{dFlat}'],
    f'C{sharp}' : [f'D{flat}'],
    'D' : [f'C{dSharp}', f'E{dFlat}'],
    f'D{sharp}' : [f'E{flat}', f'F{dFlat}'],
    'E' : [f'D{dSharp}', f'F{flat}'],
    'F' : [f'E{sharp}', f'G{dFlat}'],
    f'F{sharp}' : [f'G{flat}'],
    'G' : [f'F{dSharp}', f'A{dFlat}'],
    f'G{sharp}' : [f'A{flat}'],
    'A' : [f'G{dSharp}', f'B{dFlat}'],
    f'A{sharp}' : [f'B{flat}', f'C{dFlat}'],
    'B' : [f'A{dSharp}', f'C{flat}']}

mainNotes = [x for x in octave]
altNotes = [[y for y in octave[x]] for x in octave]

majors = ['C major', 'D major', 'E major', 'F major', 'G major', 'A major', 'B major']
minors = ['C minor', 'D minor', 'E minor', 'F minor', 'G minor', 'A minor', 'B minor']

majSharps = []
majFlats = []
minSharps = []
minFlats = []

for y in accidentalType:
    if y == sharp:
        for x in majors:
            note = x.split()
            majSharps.append((f"{note[0]}{sharp} {note[1]}"))
        for x in minors:
            note = x.split()
            minSharps.append((f"{note[0]}{sharp} {note[1]}"))
    elif y == flat:
        for x in majors:
            note = x.split()
            majFlats.append(f"{note[0]}{flat} {note[1]}")
        for x in minors:
            note = x.split()
            minFlats.append(f"{note[0]}{flat} {note[1]}")

allSharps = majSharps + minSharps
allFlats = majFlats + minFlats
allAccidentals = majSharps + majFlats + minSharps + minFlats
allNotes = allAccidentals + majors + minors

optionsDict = {'1':['Major scales', majors],
                '2':['Minor scales', minors],
                '3':[f'All sharp accidental scales ({sharp})', allSharps],
                '3a':[f'Only major sharp scales (major {sharp})', majSharps],
                '3b':[f'Only minor sharp scales (minor {sharp})', minSharps],
                '4':[f'All flat accidental scales ({flat})', allFlats],
                '4a':[f'Only major flat scales (major {flat})', majFlats],
                '4b':[f'Only minor flat scales (minor {flat})', minFlats],
                '5':['Include all of the above', allNotes]}


def difficulty(askDiff):
    notes = []
    notFound = 0
    for x in list(optionsDict.keys()):
        findKey = re.search(rf".*({x}).*", askDiff)
        if findKey != None:
            # if 'x' is found in the user input, check if there exist 'a' (or 'b') after the 'x' 
            # and if so, skip to the next 'X' in dictionary, which would be "xa"
            findSubA = re.search(rf".*({x}a).*", askDiff)
            findSubB = re.search(rf".*({x}b).*", askDiff)
            if findSubA != None or findSubB != None:
                continue
            elif findSubA == None and findSubB == None:
                notes += optionsDict[x][1]
        else:
            notFound += 1
            if notFound > len(optionsDict)-1:
                return None
    if len(notes) == 0:
        return None
    else:
        notes = set(notes)
        return notes


def askQuestion(notes):
    rndTone = rnd.randint(2, 7)
    numSuffix = ""
    notes = list(notes)
    rndNote = notes[rnd.randint(0, len(notes)-1)]
    print("Question:")
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


# -- This block of code contains all processes that are involved in finding the answer --

def giveAnswer(question):
    tone = question[0]
    note = question[1][0]
    majOrMin = question[1][1]
    answer = findAnswer(note, tone, majOrMin)
    print(f'The scale: {"  ".join(answer)}')
    print("\n-----------------------------------")
    pauseInput = input('(Press "enter" to continue or type "exit" to quit)\n')
    if pauseInput == 'exit' or pauseInput == 'q':
        sys.exit()
    print("\n"*40)
    return answer


def findAnswer(note, tone, majOrMin):
    startNote = findNote(note)
    allTones = findTone(note, tone, startNote, majOrMin)
    return allTones


def findNote(note):
    startNoteX = 0
    for x in octave:
        for y in octave[x]:
            noteRexX = re.search(rf"(^|[ ])({note})([ ]|$)", x)
            noteRexY = re.search(rf"(^|[ ])({note})([ ]|$)", y)
            if noteRexX or noteRexY:
                return startNoteX
        startNoteX += 1        


def findTone(note, tone, startNote, majOrMin):
    if majOrMin == 'major':
        scaleFormula = 'WWHWWW'
        allTones = [note]
        alphaList = allTones
        toneCount = 1 # '1' to count in the starting tone
        for step in scaleFormula:
            ans = toneSearch(allTones, step, startNote, toneCount, tone, alphaList)
            startNote = ans[0]
            allTones = ans[1]
            toneCount = ans[2]
        return allTones
    elif majOrMin == 'minor':
        scaleFormula = 'WHWWHW'
        allTones = [note]
        alphaList = allTones
        toneCount = 1
        for step in scaleFormula:
            ans = toneSearch(allTones, step, startNote, toneCount, tone, alphaList)
            startNote = ans[0]
            allTones = ans[1]
            toneCount = ans[2]
        return allTones


def toneSearch(allTones, step, startNote, toneCount, tone, alphaList):
    restartListW = startNote+2 - len(mainNotes)
    restartListH = startNote+1 - len(mainNotes)
    if step == "W":
        step = 2
        toneCount += 1
        nextNote = startNote + step
        if restartListW >= 0:
            nextNote = 0
            nextNote = restartListW
            if nextNote > len(mainNotes):
                nextNote = nextNote - len(mainNotes)
            alphabet = alphaSearch(allTones, nextNote, alphaList, step)
            allTones.append(alphabet[1])
            if toneCount == tone:
                print("-----------------------------------\n")
                print(f"Answer: {allTones[-1]}")
                return nextNote, allTones, toneCount
            return nextNote, allTones, toneCount
        else:  
            alphabet = alphaSearch(allTones, nextNote, alphaList, step)
            allTones.append(alphabet[1])
            if toneCount == tone:
                print("-----------------------------------\n")
                print(f"Answer: {allTones[-1]}")
                return nextNote, allTones, toneCount
            return nextNote, allTones, toneCount
    elif step == "H":
        step = 1
        toneCount += 1
        nextNote = startNote + step
        if restartListH >= 0:
            nextNote = 0
            nextNote = restartListH
            if nextNote >= len(mainNotes):
                nextNote = nextNote - len(mainNotes)
            alphabet = alphaSearch(allTones, nextNote, alphaList, step)
            allTones.append(alphabet[1])
            if toneCount == tone:
                print("-----------------------------------\n")
                print(f"Answer: {allTones[-1]}")
                return nextNote, allTones, toneCount
            return nextNote, allTones, toneCount
        else:
            alphabet = alphaSearch(allTones, nextNote, alphaList, step)
            allTones.append(alphabet[1])
            if toneCount == tone:
                print("-----------------------------------\n")
                print(f"Answer: {allTones[-1]}")
                return nextNote, allTones, toneCount
            return nextNote, allTones, toneCount


def alphaSearch(allTones, nextNote, alphaList, step):
    alphabet = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    countXNotes = []
    for x in mainNotes[nextNote-step:nextNote+1]:
        countXNotes.append(x)
    
    """
    # Sanity checks:
    print("\n** Notes of X axis between previous step and next note to be appended:", countXNotes)
    print("** Previous note:", allTones[-1])
    print("** Next note:", mainNotes[nextNote])
    print("** Is previous note mentioned in the steps:", allTones[-1][0] in countXNotes)
    """    

    origAlphaList = alphaList
    if allTones[-1][0] != 'B':
        oldIndex = alphabet.index(allTones[-1][0])
    else:
        oldIndex = alphabet.index('C')-1
    toneRange = oldIndex - alphabet.index(mainNotes[nextNote][0])
    if toneRange != -1:
        # checks if the note is in the alphabet list, if not, add it to the list.
        if allTones[-1][0] in countXNotes: 
            alphaList = alphaList + countXNotes
            if mainNotes[nextNote] not in " ".join(alphaList):
                return alphaList, mainNotes[nextNote]
            for x in octave[mainNotes[nextNote]]:
                if x[0] not in " ".join(alphaList):
                    return alphaList, x
            return origAlphaList, mainNotes[nextNote]
        else:
            alphaList = alphaList + [mainNotes[nextNote]]
            for x in octave[mainNotes[nextNote]]:
                if x[0] not in " ".join(alphaList):
                    return alphaList, x
            return origAlphaList, mainNotes[nextNote]
    else:
        return origAlphaList, mainNotes[nextNote]


if len(sys.argv) > 1:
    askDiff = sys.argv[1]
else:
    print("\n--------------------------------------------------\n")
    print("\t\tChoose the difficulty:\n")
    print(" Select what to include:\n")
    optList = list(optionsDict.keys())
    for x in optList:
        if re.search(r".*(.a).*", x) or re.search(r".*(.b).*", x):
            print(f"     {x} - {optionsDict[str(x)][0]}")
        else:
            print(f"  {x} - {optionsDict[str(x)][0]}")
    askDiff = input("\nInclude: ")
    print("\n--------------------------------------------------\n")

if difficulty(askDiff) != None :
    level = difficulty(askDiff)
    print("Let's begin:\n")
    while True:
        try:
            question = askQuestion(level)
            pauseInput = input("")
            if pauseInput == 'exit' or pauseInput == 'q':
                print("\nGoodbye\n")
                break
            giveAnswer(question)
        except:
            print("\nGoodbye\n")
            sys.exit()
else:
    print("\nGoodbye\n")
