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

def alignRes(answer):
    for x in answer:
        answer[answer.index(x)] = (x).ljust(4)
    return answer


def simplify(givenNotes):
    if f"{dSharp}" in givenNotes:
        givenNotes = givenNotes[0] + "##"
    elif f"{dFlat}" in givenNotes:
        givenNotes = givenNotes[0] + "bb"
    elif f"{sharp}" in givenNotes:
        givenNotes = givenNotes[0] + "#"
    elif f"{flat}" in givenNotes:
        givenNotes = givenNotes[0] + "b"
    return givenNotes


def checkAnswer(xrcType, tone, pauseAns, foundAns):
    if xrcType == 1:
        alphaAns = foundAns[1]
        simpleAns = simplify(foundAns[0][tone-1])
        if pauseAns:
            if pauseAns.casefold() != simpleAns.casefold() and (pauseAns.casefold() in [simplify(x.casefold()) for x in octave[f'{alphaAns[tone-1]}']] or pauseAns.casefold() == simplify(alphaAns[tone-1].casefold())):
                print(f'{("Your answer :").rjust(len("Relative Minor :"))}', f'"{pauseAns}" - Enharmonically correct, but not notation-wise({foundAns[0][tone-1]})\n')
            elif pauseAns.casefold() == simpleAns.casefold():
                print(f'{("Your answer :").rjust(len("Relative Minor :"))}', f'"{pauseAns}" - Correct\n')
            else:
                print(f'{("Your answer :").rjust(len("Relative Minor :"))}', f'"{pauseAns}" - Incorrect\n')
    elif xrcType == 2:
        if pauseAns:
            if [simplify(x.casefold()) for x in pauseAns] == [simplify(x.casefold()) for x in foundAns[0]]:
                print(f'{("Your answer :").rjust(len("Relative Minor :"))}', f'"{" ".join(pauseAns)}" - Correct\n')
            else:
                print(f'{("Your answer :").rjust(len("Relative Minor :"))}', f'"{" ".join(pauseAns)}" - Incorrect\n')


def giveAnswer(question, pauseAns, xrcType):
    tone = question[0] # a tone to find. ex.: 6
    note = question[1][0] # a root note of the scale. ex.: 'F'
    majOrMin = question[1][1] # ex.: 'major' or 'minor'
    foundAns = findAnswer(note, tone, majOrMin) # rt.: (['E♭', 'F', 'G♭',...] , ['D♯', 'F', 'F♯',...])
    checkAnswer(xrcType, tone, pauseAns, foundAns) # doesn't return anything, only prints
    answer = alignRes(foundAns[0]) # rt.: ['B   ', 'C♯  ', 'D   ',...]
    ruler = []
    rcount = 0
    for x in answer:
        rcount += 1
        ansLen = len(answer[answer.index(x)])
        ruler.append(str(rcount).ljust(ansLen))
    print(f'{"|".rjust(len("Relative Minor :"))} {"".join(ruler)}')
    print(f'{("Scale :").rjust(len("Relative Minor :"))} {"".join(answer)}')
    
    # finds relative minor and major
    if majOrMin == 'major':
        relMinor = alignRes(findAnswer(answer[-3].strip(), -1, 'minor')[0])
        print(f'{(f"Relative Minor :").rjust(len("Relative Minor :"))} {"".join(relMinor)}')
    elif majOrMin == 'minor':
        relMinor = alignRes(findAnswer(answer[-6].strip(), -1, 'major')[0])
        print(f'{(f"Relative Major :").rjust(len("Relative Minor :"))} {"".join(relMinor)}')
    print("\n-----------------------------------")
    pauseInput = input('(Press "enter" to continue or type "exit" to quit)\n')
    if pauseInput == 'exit' or pauseInput == 'quit' or pauseInput == 'q':
        sys.exit()
    print("\n"*40)
    return answer


def findAnswer(note, tone, majOrMin):
    startNote = findNote(note) # rt.: an index of a root note in 'octave'. ex.: 0 - 11
    allTones = findTone(note, tone, startNote, majOrMin) # ['B', 'C♯', 'D',...] , ['C', 'D', 'E', 'F', 'G',...]  <--- ('allTones' , 'alphaAns')
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
        scaleFormula = 'WWHWWWH'
        allTones = [note]
        alphaList = [mainNotes[startNote]] # 'alphaList' will keep track of actual "key(or string) that is played", while 'allTones' keeps correct notation for that key
        toneCount = 1 # '1' to count in the starting tone
        for step in scaleFormula:
            ans = toneSearch(allTones, step, startNote, toneCount, tone, alphaList)
            startNote = ans[0]
            allTones = ans[1]
            toneCount = ans[2]
            alphaAns = ans[3] # <--- 'alphaList'
        return allTones, alphaAns
    elif majOrMin == 'minor':
        scaleFormula = 'WHWWHWW'
        allTones = [note]
        alphaList = [mainNotes[startNote]]
        toneCount = 1
        for step in scaleFormula:
            ans = toneSearch(allTones, step, startNote, toneCount, tone, alphaList)
            startNote = ans[0]
            allTones = ans[1]
            toneCount = ans[2]
            alphaAns = ans[3] # <--- 'alphaList'
        return allTones, alphaAns


def makeStep(allTones, step, startNote, toneCount, tone, alphaList, restartList):
    if tone > 1:
        toneCount += 1
    nextNote = startNote + step
    if restartList >= 0:
        nextNote = 0
        nextNote = restartList
        if nextNote > len(mainNotes):
            nextNote = nextNote - len(mainNotes)
        alphabet = alphaSearch(allTones, nextNote, alphaList) # ['B', 'C♯', ..., 'F♯'] , F♯
        allTones.append(alphabet[1])
        if xrcType == 1:
            if toneCount == tone and tone > -1:
                print("-----------------------------------\n")
                print(f'{("Answer :").rjust(len("Relative Minor :"))} {"".join(allTones[-1])}\n')
        elif xrcType == 2 and toneCount == 8:
            print(f'{("Answer :").rjust(len("Relative Minor :"))} {" ".join(allTones)}\n')
        return nextNote, allTones, toneCount
    else:
        alphabet = alphaSearch(allTones, nextNote, alphaList) # ['B', 'C♯', ..., 'F♯'] , F♯
        allTones.append(alphabet[1])
        if xrcType == 1:
            if toneCount == tone and tone > -1 and xrcType == 1:
                print("-----------------------------------\n")
                print(f'{("Answer :").rjust(len("Relative Minor :"))} {"".join(allTones[-1])}\n')
        elif xrcType == 2 and toneCount == 8:
            print(f'{("Answer :").rjust(len("Relative Minor :"))} {" ".join(allTones)}\n')
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
        return nextNote, allTones, toneCount, alphaList
    elif step == "H":
        step = 1
        madeStep = makeStep(allTones, step, startNote, toneCount, tone, alphaList, restartListH)
        nextNote = madeStep[0]
        allTones = madeStep[1]
        toneCount = madeStep[2]
        return nextNote, allTones, toneCount, alphaList


def alphaSearch(allTones, nextNote, alphaList):
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

def askXrc():
    while True:
        xrc = input("\nChoose exercise:\n1 - Find Tone\n2 - Write Out Scales\nExercise: ")
        if (0 < len(xrc) < 2) and re.search(r"(^[1-2])", xrc) :
            if xrc == '1':
                return 1 # find tone
            elif xrc == '2':
                return 2 # write out scales
        else:
            print("* Please enter a valid option")
                


def diffSelector(options):
    print("\n--------------------------------------------------\n")
    print("\t\tChoose the difficulty:\n")
    print(" Select what to include:\n")
    optList = list(options.keys())
    for x in optList:
        if re.search(r".*(.a).*", x) or re.search(r".*(.b).*", x):
            print(f"     {x} - {options[str(x)][0]}")
        else:
            print(f"  {x} - {options[str(x)][0]}")
    difficulty = input("\nInclude: ")
    print("\n--------------------------------------------------\n")
    return difficulty


def selectLevel(diff):
    notes = []
    notFound = 0
    for x in list(diffOptions.keys()):
        findKey = re.search(rf".*({x}).*", diff)
        if findKey != None:
            # if 'x' is found in the user input, check if there exist 'a' (or 'b') after the 'x'
            # and if so, skip to the next 'X' in dictionary, which would be "xa"
            findSubA = re.search(rf".*({x}a).*", diff)
            findSubB = re.search(rf".*({x}b).*", diff)
            if findSubA != None or findSubB != None:
                continue
            elif findSubA == None and findSubB == None:
                notes += diffOptions[x][1]
                print(f'* {diffOptions[x][0]}')
        else:
            notFound += 1
            if notFound > len(diffOptions)-1:
                print("Invalid option.")
                return None
    if len(notes) == 0:
        print("Invalid option.")
        return None
    else:
        if len(notes) > 7:
            print("Removing duplicates..")
        notes = set(notes)
        return notes


def askQuestion(xrc, notes):
    rndTone = rnd.randint(2, 7) # 2 - 7
    numSuffix = ""
    notes = list(notes)
    rndNote = notes[rnd.randint(0, len(notes)-1)]
    if xrc == 1:
        print("Question:")
        if rndTone == 1: # 1st and 8th tones aren't really used as specified above
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
    elif xrc == 2:
        print(f"\nWrite out {rndNote} scale:\n")
        return rndTone, rndNote.split()


def giveCheats(octave):
    mList = ['major', 'minor']
    for z in mList:
        print(f'\n\n{(z.upper()).rjust(31)}')
        for x in octave:
            ansScale = alignRes(findAnswer(x.strip(), -1, z)[0])
            cheatStringLen = len(f'  {((ansScale[0]).ljust(4))}|  {"-  ".join(ansScale)}')
            print(f"\n{('(').rjust(int(cheatStringLen/2.25))} {ansScale[0].strip()} )")
            ruler = []
            rcount = 0
            for p in ansScale:
                rcount += 1
                ansLen = len(ansScale[ansScale.index(p)])
                ruler.append(("(" + str(rcount) + ")").ljust(ansLen))
            introLen = len(f'{((ansScale[0]).ljust(6))}|')
            print(f'{"|".rjust(introLen)} {"   ".join(ruler)}')
            print(f'  {((ansScale[0]).ljust(4))}|  {"-  ".join(ansScale)}')
            for y in octave[x]:
                if f'{sharp}{dSharp}' in y or f'{flat}{dFlat}' in y:
                    continue
                else:
                    ansScale = alignRes(findAnswer(y, -1, z)[0])
                    print(f'  {((ansScale[0]).ljust(4))}|  {"-  ".join(ansScale)}')
        print("\n")



# Searches for any arguments(numbers and letters) passed to the program. If found: numbers are returned in 'foundNum', letters in 'foundArg' 
def argFunc(diffOptions):
    maxOption = max([x for x in diffOptions])
        # searching for numeric argument for difficulty
    numSearch = re.compile(rf".?([1-{maxOption}]).?")
    foundNum = "".join(list("".join(filter(numSearch.findall, sys.argv[1:]))))
        # searching for supplementary arguments
    argSearch = re.compile(r"\-(.+)", re.I)
    foundArg = list("".join(filter(argSearch.findall, sys.argv[1:])))
    for x in foundArg:
        if x == '-': # eliminates '-' from the arguments list
            foundArg.pop(foundArg.index(x))
    if foundArg:
        if 'b' in "".join(foundArg):
            print("* Basic Notes - Enabled")
    return foundArg, foundNum

def pauseInput(xrc):
    if xrc == 1:
        pauseInp = input("\nYour answer(optional): ")
        return pauseInp
    elif xrc == 2:
        pauseInp = input("\nYour answer(space separated): ")
        pauseInp = pauseInp.split()
        return pauseInp


def showtime(diff, xrcType):
    level = selectLevel(diff) # rt.: {'E major', 'F♯ minor', 'B♭ minor', 'C♯ major',...}
    if level == None:
        print("\nGoodbye\n")
        sys.exit()
    print("\nLet's begin:\n")
    while True:
        try:
            question = askQuestion(xrcType, level) # 4 , ['F♭', 'minor']
            pauseAns = pauseInput(xrcType)
            print("\n")
            if pauseAns == 'exit' or pauseAns == 'quit' or pauseAns == 'q':
                print("\nGoodbye\n")
                sys.exit()
            giveAnswer(question, pauseAns, xrcType)
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
octave = firstArgs[0] # {..., 'C♯': ['B𝄪', 'D♭', 'E♭𝄫'],...}
mainNotes = firstArgs[1] # ['C', 'C♯', 'D', 'D♯', 'E',...] 
diffOptions = firstArgs[2] # {'1': ['Major scales', ['C major', 'D major',...]]}
arguments = argFunc(diffOptions) # ['b','c'] , '4b'



if 'b' in arguments[0]:
    natural = ''
    sharp = '#'
    flat = 'b'
    dSharp = '##'
    dFlat = 'bb'
    accidentalType = ['#', 'b', '##', 'bb']
    firstArgs = startFunc(natural, sharp, flat, dSharp, dFlat, accidentalType)
    octave = firstArgs[0]
    mainNotes = firstArgs[1]
    diffOptions = firstArgs[2]

if 'c' in arguments[0]:
    octave = firstArgs[0]
    mainNotes = firstArgs[1]
    xrcType = 1
    giveCheats(octave)
    sys.exit()

if 's' in arguments[0]:
    octave = firstArgs[0]
    mainNotes = firstArgs[1]


if arguments[1]: # "if user passed 'difficulty' argument"
    diff = arguments[1]
    try:
        xrcType = askXrc()
    except:
        print("\nGoodbye\n")
        sys.exit()
    showtime(diff, xrcType)
else:
    try:
        xrcType = askXrc()
        diff = diffSelector(diffOptions)
    except:
        print("\nGoodbye\n")
        sys.exit()        
    showtime(diff, xrcType)
    
