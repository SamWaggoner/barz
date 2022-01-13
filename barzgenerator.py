# this is an added new comment

# Bars Generator Remade
# import webbrowser
# webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
import datamuse
import random
import requests
import os
from gtts import gTTS

api = datamuse.Datamuse()
# word = "chrosome"

# use jja or jjb if random word doesn't work well? test first with chromosome

# rhymes = api.words(rel_rhy=word, max=15)
# choice = random.randint(0,len(rhymes)-1)
# print(rhymes[choice]["word"])

# homophones = api.words(rel_hom=word, max=15)
# choice = random.randint(0,len(homophones)-1)
# print(homophones[choice]["word"])

# predecessors = api.words(rel_bgb=word)
# print(predecessors)
# choice = random.randint(0,len(predecessors)-1)
# print(predecessors[choice]["word"])

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
    rhymes = api.words(rel_rhy=rhymeWord) # get list of rhyming words using datamuse library. default max length of rhymes is 100
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

    return usedRhymes

def main():
    # get inputs, sanitize
    rhymeWord = input("What u wanna rhyme with, make it timeless (any single word): ")
    maxSyllables = input("How many syllables per line, u lookin fine: ")
    try:
        maxSyllables = int(maxSyllables)
    except TypeError or ValueError:
        print("Please enter an integer number for the number of syllables per line.")
        main()
    barsNum = input("How many bars u want: ")
    try:
        barsNum = int(barsNum)
    except TypeError or ValueError:
        print("Please enter an integer number for the number of bars.")
        main()
    rhymeScheme = input("What type of rhyme scheme would you like to redeem: \
        \n\t1. Classic: AAAA scheme, rhymes at the end of every line  \
        \n\t2. Sonnet: 14 lines, 10 syllables per line  \
        \n\t3. Rough Haiku: 3 lines, syllables 5,7,5 per line  \
        \n\t4. Pentameter: 5 syllables per line (can't do iambic, sorry)  \
        \n\t5. Limerick: 5 lines, AABBA scheme \
        \n\t6. Villanelle: 19 lines, comprising 5 tercets (ABA) and a quatrain (ABAA): \
        \n\t      A1 b A2 / a b A1 / a b A2 / a b A1 / a b A2 / a b A1 A2, capital = refrain \
        \n\tNote: syllables are imperfect.")
    try:
        rhymeScheme = int(rhymeScheme)
    except TypeError or ValueError:
        print("Please enter an integer number for your selection.")
        main()
    if rhymeScheme < 1 or rhymeScheme > 6:
        print("Invalid selection.")
        main()
        
    # clear the barz.txt file of previous bars
    file = open("barz.txt,","w")
    file.close()

    # generate the bars
    print("Bars:")
    usedRhymes = []
    for i in range(barsNum):
        usedRhymes = makeBar(rhymeWord,maxSyllables,usedRhymes)

    # readAloud("barz.txt")

main()







"""
end the line with homonyms or rhymes
use rhyme schemes
"""


