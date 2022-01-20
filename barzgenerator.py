# Bars Generator V2
# Samuel Waggoner
# December 2021 - Current

# Repo: https://github.com/SamWaggoner/rhymes

import random
import requests
import os

# from gtts import gTTS # for reading out loud, raises an error

def readAloud(fileName):
    file = open(fileName,"r")
    file = file.read().replace("\n",",,,")
    language = "en"
    speech = gTTS(text = str(file), lang = language, slow = False)
    speech.save("barz.mp3")
    os.system("start barz.mp3")

def selectPredecessor(predecessors, currSyl, maxSyl):
    choiceNum = random.randint(0,len(predecessors)-1)
    choice = predecessors[choiceNum]
    if choice["numSyllables"] + currSyl > maxSyl:
        del predecessors[choiceNum]
        return selectPredecessor(predecessors,currSyl,maxSyl)
    else:
        return choice

def addPredecessors(bar,word,currSyl,maxSyl,failCount=0):
    url = "https://api.datamuse.com/words?rel_bgb=" + str(word) + "&md=s"
    response = requests.get(url)
    predecessors = response.json()
    if len(predecessors) == 0:
        print("Sorry, can't find no words for this here turd: " + str(word))
        return -1
    choice = selectPredecessor(predecessors,currSyl,maxSyl)
    currSyl += choice["numSyllables"]
    newWord = choice["word"]
    newBar = newWord + " " + bar
    if currSyl == maxSyl:
        return bar
    else:
        return addPredecessors(newBar,newWord,currSyl,maxSyl,0)

def makeBar(rhymeWord, maxSyllables, usedRhymes = []): # usedRhymes is list of already used rhymes to prevent repeats
    bar = ""
    currSyllables = 0 # syllable count starts at 0, not to exceed max syllables per line as given by user
    url = "https://api.datamuse.com/words?rel_rhy=" + rhymeWord + "&md=s"
    response = requests.get(url)
    rhymes = response.json()

    if len(rhymes) == 0: # if there are no rhymes for the word
        print("Sorry, can't find any rhymes for %s in this amount of time" %rhymeWord)
        exit()

    # find an unused rhyme for the word
    choiceNum = random.randint(0,len(rhymes)-1)
    # while (the chosen word is already used or the chosen word is not a single word) and the rhymes list is not exhaused:
    while (rhymes[choiceNum]["word"] in usedRhymes or len(rhymes[choiceNum]["word"].split(" ")) > 1):
        del rhymes[choiceNum]
        if len(rhymes) == 0: # if there are no rhymes for the word that aren't alredy used or one word
            print("Sorry, can't find any rhymes for %s in this amount of time" %rhymeWord)
            exit()
        choiceNum = random.randint(0,len(rhymes)-1)
    choiceWord = rhymes[choiceNum]["word"]
    usedRhymes.append(choiceWord)
    bar = bar + choiceWord # bar is now the rhyme

    # creates the rest of the bar (words before the rhyme word)
    bar = addPredecessors(bar,choiceWord,currSyllables,maxSyllables)

    print(bar)

    # write the bar in the file
    file = open("barz.txt,","a")
    file.write("\n"+str(bar))
    file.close()

    return usedRhymes,bar

def getRandomWord():
    startChars = "abcdefghijklmnopqrstuvwxyz"
    startChar = random.choice(startChars)
    url = "https://api.datamuse.com/words?sp=%s*" %startChar
    response = requests.get(url)
    responses = response.json()
    return responses[random.randint(0,len(responses))]["word"]

def getUserRhyme():
    rhymeWord = input("What u wanna rhyme with, make it timeless (any single word): ")
    return rhymeWord

def getUserMaxSyllables():
    maxSyllables = input("How many syllables per line, make it fine: ")
    try:
        return int(maxSyllables)
    except ValueError or TypeError:
        print("Please enter an integer number for the number of syllables per line.")
        return getUserMaxSyllables()

def getUserBarsNum():
    barsNum = input("How many bars u want: ")
    try:
        return int(barsNum)
    except ValueError or TypeError:
        print("Please enter an integer number for the number of bars.")
        return getUserBarsNum()

def main():

    # main directory of intention
    rhymeScheme = input("What type of rhyme scheme do u wanna redeem: \
    \n\t1. Classic: AAAA scheme, rhymes at the end of every line  \
    \n\t2. Sonnet: 14 lines, 10 syllables per line  \
    \n\t3. Rough Haiku: 3 lines, syllables 5,7,5 per line  \
    \n\t4. Pentameter: 5 syllables per line (can't do iambic, sorry)  \
    \n\t5. Limerick: 5 lines, AABBA scheme \
    \n\t6. Villanelle: 19 lines, comprising 5 tercets (ABA) and a quatrain (ABAA): \
    \n\t      A1 b A2 / a b A1 / a b A2 / a b A1 / a b A2 / a b A1 A2, capital = refrain \
    \n\tPlease enter your choice's number. Note: syllables are imperfect. \
    \n->")
    try:
        rhymeScheme = int(rhymeScheme)
    except TypeError or ValueError:
        print("Please enter an integer number for your selection.")
        main()
    if rhymeScheme < 1 or rhymeScheme > 6:
        print("Invalid selection.")
        main()

    # clear the barz.txt file of previous bars
    file = open("barz.txt","w")
    file.close()

    # Classic AAAA
    if rhymeScheme == 1:
        rhymeWord = getUserRhyme()
        numSyllables = getUserMaxSyllables()
        barsNum = getUserBarsNum()
        # generate the bars
        print("Bars:")
        usedRhymes = []
        for i in range(barsNum):
            usedRhymes = makeBar(rhymeWord,numSyllables,usedRhymes)[0]

    # Sonnet: 14 lines, 10 syllables per line: ABAB, CDCD, EFEF, GH
    elif rhymeScheme == 2:
        rhymeWordA = getRandomWord()
        rhymeWordB = getRandomWord()
        rhymeWordC = getRandomWord()
        rhymeWordD = getRandomWord()
        rhymeWordE = getRandomWord()
        rhymeWordF = getRandomWord()
        rhymeWordG = getRandomWord()
        rhymeWordH = getRandomWord()
        numSyllables = getUserMaxSyllables()

        print("Bars:")
        usedRhymes = []
        usedRhymes = makeBar(rhymeWordA,numSyllables,usedRhymes)[0]
        usedRhymes = makeBar(rhymeWordB,numSyllables,usedRhymes)[0]
        makeBar(rhymeWordA,numSyllables,usedRhymes)
        makeBar(rhymeWordB,numSyllables,usedRhymes)

        usedRhymes = makeBar(rhymeWordC,numSyllables,usedRhymes)[0]
        usedRhymes = makeBar(rhymeWordD,numSyllables,usedRhymes)[0]
        makeBar(rhymeWordC,numSyllables,usedRhymes)
        makeBar(rhymeWordD,numSyllables,usedRhymes)

        usedRhymes = makeBar(rhymeWordE,numSyllables,usedRhymes)[0]
        usedRhymes = makeBar(rhymeWordF,numSyllables,usedRhymes)[0]
        makeBar(rhymeWordE,numSyllables,usedRhymes)
        makeBar(rhymeWordF,numSyllables,usedRhymes)

        makeBar(rhymeWordG,numSyllables,usedRhymes)
        makeBar(rhymeWordH,numSyllables,usedRhymes)

    # Rough Haiku: 3 lines, syllables 5,7,5 per line
    elif rhymeScheme == 3:
        print("The datamuse API guesses number of syllables if it is not given...\
        \n so this is not very accurate :)")
        randomWordA = getRandomWord()
        randomWordB = getRandomWord()
        randomWordC = getRandomWord()
        makeBar(randomWordA,5)
        makeBar(randomWordA,7)
        makeBar(randomWordA,5)

    # Pentameter: 5 syllables per line
    elif rhymeScheme == 4:
        numBars = getUserBarsNum()
        usedRhymes = []
        for i in range(numBars):
            rhymeWord = getUserRhyme()
            usedRhymes = makeBar(rhymeWord,5,usedRhymes)[0]

    # Limerick: 5 lines, AABBA scheme
    elif rhymeScheme == 5:
        maxSyllables = getUserMaxSyllables()
        rhymeWordA = getUserRhyme()
        rhymeWordB = getUserRhyme()
        usedRhymes = []
        for i in range(2):
            usedRhymes = makeBar(rhymeWordA,maxSyllables,usedRhymes)[0]
        for i in range(2):
            usedRhymes = makeBar(rhymeWordB,maxSyllables,usedRhymes)[0]
        makeBar(rhymeWordA,maxSyllables,usedRhymes)
    
    # Villanelle: 19 lines, comprising 5 tercets (ABA) and a quatrain (ABAA):
    # A1 b A2 / a b A1 / a b A2 / a b A1 / a b A2 / a b A1 A2, capital = refrain
    elif rhymeScheme == 6:
        usedRhymes = []
        a1Word = getRandomWord()
        a2Word = getRandomWord()
        aWord = getRandomWord()
        bWord = getRandomWord()
        syl = random.randint(4,10)
        
        res1 = makeBar(a1Word,syl,usedRhymes)
        usedRhymes = res1[0]
        a1 = res1[1]
        usedRhymes = makeBar(bWord,syl,usedRhymes)[0]
        res2 = makeBar(a2Word,syl,usedRhymes)
        usedRhymes = res2[0]
        a2 = res2[1]
        print(a1)
        print(a2)

        for i in range(2):
            usedRhymes = makeBar(aWord,syl,usedRhymes)[0]
            usedRhymes = makeBar(bWord,syl,usedRhymes)[0]
            print(a1)

            usedRhymes = makeBar(aWord,syl,usedRhymes)[0]
            usedRhymes = makeBar(bWord,syl,usedRhymes)[0]
            print(a2)

        usedRhymes = makeBar(aWord,syl,usedRhymes)[0]
        usedRhymes = makeBar(bWord,syl,usedRhymes)[0]
        print(a1)
        print(a2)
        



    # readAloud("barz.txt")

main()

# if you want to Rickroll someone then use the code below
# import webbrowser
# webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Repo: https://github.com/SamWaggoner/rhymes