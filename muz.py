#!/usr/bin/env python3

import random as rnd
import sys, re

def startFunc(natural, sharp, flat, dSharp, dFlat, accidentalType):
    octave = {
        'C' : [f'A{sharp}{dSharp}', f'B{sharp}', f'D{dFlat}'],
        f'C{sharp}' : [f'B{dSharp}', f'D{flat}', f'E{flat}{dFlat}'],
        'D' : [f'C{dSharp}', f'E{dFlat}'],
        f'D{sharp}' : [f'C{sharp}{dSharp}', f'E{flat}', f'F{dFlat}', f'F{flat}{dFlat}'],
        'E' : [f'D{dSharp}', f'F{flat}'],
        'F' : [f'D{sharp}{dSharp}', f'E{sharp}', f'G{dFlat}'],
        f'F{sharp}' : [f'E{dSharp}', f'G{flat}', f'A{flat}{dFlat}'],
        'G' : [f'F{dSharp}', f'A{dFlat}'],
        f'G{sharp}' : [f'F{sharp}{dSharp}', f'A{flat}', f'B{flat}{dFlat}'],
        'A' : [f'G{dSharp}', f'B{dFlat}'],
        f'A{sharp}' : [f'G{sharp}{dSharp}', f'B{flat}', f'C{dFlat}'],
        'B' : [f'A{dSharp}', f'C{flat}']}

    mainNotes = [x for x in octave]

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
                    '5':['Everything', allNotes]}
    return octave, mainNotes, optionsDict


# -- This block of code contains all processes that are involved in finding the answers --

def giveAnswer(question):
    tone = question[0]
    note = question[1][0]
    majOrMin = question[1][1]
    answer = findAnswer(note, tone, majOrMin)
    print(f'{("Scale :").rjust(len("Relative Minor :"))} {"  ".join(answer)}')
    # finds relative minor and major
    if majOrMin == 'major':
        relMinor = findAnswer(answer[-2], -1, 'minor')
        print(f'{(f"Relative Minor :").rjust(len("Relative Minor :"))} {"  ".join(relMinor)}')
    elif majOrMin == 'minor':
        relMinor = findAnswer(answer[-5], -1, 'major')
        print(f'{(f"Relative Major :").rjust(len("Relative Minor :"))} {"  ".join(relMinor)}')
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
        alphaList = [mainNotes[startNote]]
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
        alphaList = [mainNotes[startNote]]
        toneCount = 1
        for step in scaleFormula:
            ans = toneSearch(allTones, step, startNote, toneCount, tone, alphaList)
            startNote = ans[0]
            allTones = ans[1]
            toneCount = ans[2]
        return allTones


def makeStep(allTones, step, startNote, toneCount, tone, alphaList, restartList):
    if tone > 1:
        toneCount += 1
    nextNote = startNote + step
    if restartList >= 0:
        nextNote = 0
        nextNote = restartList
        if nextNote > len(mainNotes):
            nextNote = nextNote - len(mainNotes)
        alphabet = alphaSearch(allTones, nextNote, alphaList, step)
        allTones.append(alphabet[1])
        if toneCount == tone and tone > -1:
            print("-----------------------------------\n")
            print(f'{("Answer :").rjust(len("Relative Minor :"))} {"".join(allTones[-1])}\n')
        return nextNote, allTones, toneCount
    else:
        alphabet = alphaSearch(allTones, nextNote, alphaList, step)
        allTones.append(alphabet[1])
        if toneCount == tone and tone > -1:
            print("-----------------------------------\n")
            print(f'{("Answer :").rjust(len("Relative Minor :"))} {"".join(allTones[-1])}\n')
        return nextNote, allTones, toneCount


def toneSearch(allTones, step, startNote, toneCount, tone, alphaList):
    restartListW = startNote+2 - len(mainNotes)
    restartListH = startNote+1 - len(mainNotes)
    if step == "W":
        step = 2
        madeStep = makeStep(allTones, step, startNote, toneCount, tone, alphaList, restartListW)
        nextNote = madeStep[0]
        allTones = madeStep[1]
        toneCount = madeStep[2]
        return nextNote, allTones, toneCount
    elif step == "H":
        step = 1
        madeStep = makeStep(allTones, step, startNote, toneCount, tone, alphaList, restartListH)
        nextNote = madeStep[0]
        allTones = madeStep[1]
        toneCount = madeStep[2]
        return nextNote, allTones, toneCount


def alphaSearch(allTones, nextNote, alphaList, step):
    alphabet = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    """
    # Sanity checks:
    print("** Current note:", allTones[-1])
    print("** Next X-axis note:", mainNotes[nextNote])
    if allTones[-1][0] == 'B':
        print("** Next Y-axis note should be:", alphabet[alphabet.index('C')])
    else:
        print("** Next Y-axis note should be:", alphabet[alphabet.index(allTones[-1][0])+1])
    """
    
    if allTones[-1][0] == 'B':
        for y in octave[mainNotes[nextNote]]:
            if y[0] == 'C':
                alphaList.append(mainNotes[nextNote])
                return alphaList, y
    else:
        for y in octave[mainNotes[nextNote]]:
            if y[0] == alphabet[alphabet.index(allTones[-1][0])+1]:
                alphaList.append(mainNotes[nextNote])
                return alphaList, y
    
    alphaList.append(mainNotes[nextNote])
    return alphaList, mainNotes[nextNote]


# -- This block of code contains all processes that are involved in asking the questions --

def askMenu(options):
    print("\n--------------------------------------------------\n")
    print("\t\tChoose the difficulty:\n")
    print(" Select what to include:\n")
    optList = list(options.keys())
    for x in optList:
        if re.search(r".*(.a).*", x) or re.search(r".*(.b).*", x):
            print(f"     {x} - {options[str(x)][0]}")
        else:
            print(f"  {x} - {options[str(x)][0]}")
    askDiff = input("\nInclude: ")
    print("\n--------------------------------------------------\n")
    return askDiff


def difficulty(askDiff, options):
    notes = []
    notFound = 0
    for x in list(options.keys()):
        findKey = re.search(rf".*({x}).*", askDiff)
        if findKey != None:
            # if 'x' is found in the user input, check if there exist 'a' (or 'b') after the 'x'
            # and if so, skip to the next 'X' in dictionary, which would be "xa"
            findSubA = re.search(rf".*({x}a).*", askDiff)
            findSubB = re.search(rf".*({x}b).*", askDiff)
            if findSubA != None or findSubB != None:
                continue
            elif findSubA == None and findSubB == None:
                notes += options[x][1]
                print(f'** {options[x][0]}')
        else:
            notFound += 1
            if notFound > len(options)-1:
                return None
    if len(notes) == 0:
        return None
    else:
        if len(notes) > 7:
            print("Removing duplicates..")
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


def giveCheats(octave):
    mList = ['major', 'minor']
    for z in mList:
        print(f'\n\n{(z.upper()).rjust(24)}')
        for x in octave:
            ansScale = findAnswer(x, -1, z)
            print(f"\n{('(').rjust(20)} {ansScale[0]} )")
            print(f'  {((ansScale[0]).ljust(4))}|  {" - ".join(ansScale)}')
            for y in octave[x]:
                if f'{sharp}{dSharp}' in y or f'{flat}{dFlat}' in y:
                    continue
                else:
                    ansScale = findAnswer(y, -1, z)
                    print(f'  {((ansScale[0]).ljust(4))}|  {" - ".join(ansScale)}')
        print("\n")


def argFunc(optionsDict):
    maxOption = max([x for x in optionsDict])
        # searching for numeric argument for difficulty
    diffSearch = re.compile(rf".?([1-{maxOption}]).?")
    foundDiff = "".join(list("".join(filter(diffSearch.findall, sys.argv[1:]))))
        # searching for supplementary arguments
    argSearch = re.compile(r"\-(.+)", re.I)
    foundArg = list("".join(filter(argSearch.findall, sys.argv[1:])))
    for x in foundArg:
        if x == '-' or x.isnumeric():
            foundArg.pop(foundArg.index(x))
    if foundArg:
        if 'b' in "".join(foundArg):
            print("Basic Notes - Enabled")
    return foundArg, foundDiff


def showTime(askDiff, options):
    level = difficulty(askDiff, options)
    if level == None:
        print("\nGoodbye\n")
        sys.exit()
    print("\nLet's begin:\n")
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



# -- execution starts here

natural = b'\xe2\x99\xae'.decode('utf-8')
sharp = b'\xe2\x99\xaf'.decode('utf-8')
flat = b'\xe2\x99\xad'.decode('utf-8')
dSharp = b'\xf0\x9d\x84\xaa'.decode('utf-8')
dFlat = b'\xf0\x9d\x84\xab'.decode('utf-8')
accidentalType = [natural, sharp, flat, dSharp, dFlat]

firstArgs = startFunc(natural, sharp, flat, dSharp, dFlat, accidentalType)
octave = firstArgs[0]
mainNotes = firstArgs[1]
options = firstArgs[2]
arguments = argFunc(options)

if 'b' in arguments[0]:
    natural = ''
    sharp = '#'
    flat = 'b'
    dSharp = '##'
    dFlat = 'bb'
    accidentalType = ['#', 'b', '##', 'bb']
    if 'c' in arguments[0]:
        firstArgs = startFunc(natural, sharp, flat, dSharp, dFlat, accidentalType)
        octave = firstArgs[0]
        mainNotes = firstArgs[1]
        giveCheats(octave)
        sys.exit()
    else:
        if arguments[1]:
            firstArgs = startFunc(natural, sharp, flat, dSharp, dFlat, accidentalType)
            octave = firstArgs[0]
            mainNotes = firstArgs[1]
            options = firstArgs[2]
            askDiff = arguments[1]
            showTime(askDiff, options)
        else:
            firstArgs = startFunc(natural, sharp, flat, dSharp, dFlat, accidentalType)
            octave = firstArgs[0]
            mainNotes = firstArgs[1]
            options = firstArgs[2]
            askDiff = askMenu(options)
            showTime(askDiff, options)
else:
    if 'c' in arguments[0]:
        firstArgs = startFunc(natural, sharp, flat, dSharp, dFlat, accidentalType)
        octave = firstArgs[0]
        mainNotes = firstArgs[1]
        giveCheats(octave)
        sys.exit()
    else:
        if arguments[1]:
            askDiff = arguments[1]
            showTime(askDiff, options)
        else:
            askDiff = askMenu(options)
            showTime(askDiff, options)
