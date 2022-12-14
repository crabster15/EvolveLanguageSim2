from xml.dom import minidom
import xml.etree.ElementTree as gfg 
import os
import string
import random as rd
from random_word import RandomWords
import argparse

#set flags for words 
parser = argparse.ArgumentParser()

parser.add_argument('--MaxWordLength', type=int, required=True)
parser.add_argument('--AmountOfWords', type=int, required=True)
parser.add_argument('--MaxAmountOfVowels', type=int, required=True)
parser.add_argument('--FileName', type=str, required=True)

args = parser.parse_args()

r = RandomWords()

root = minidom.Document()
  
root = gfg.Element("Dictionary")
      

#for each word add to xml
for i in range(0, args.AmountOfWords):

    #create a random word
    wordLen = rd.randint(1,args.MaxWordLength)
    word = (''.join(rd.choices(string.ascii_uppercase + string.ascii_lowercase, k=wordLen)))

    #select the vowels
    amountVowels = rd.randint(1, 4)
    vowelList = ""
    for i in range(0, amountVowels):
        #select 2 char vowel or make 1 vowel
        vowel = rd.choice(word)
        index = rd.randint(0,2)
        if(index == 0):
            if(word.index(vowel) < len(word) - 1):
                vowel +=  word[word.index(vowel) + 1]
        elif(index == 1):
            if(word.index(vowel) > 0):
                vowel =  word[word.index(vowel) - 1] + vowel
        

        #ATTENTION this hack is suspicious because the script has ocassional errors when the
        #if the vowel is already in the list delete it
        #vowelList = vowelList.replace(vowel+',', "") 
        vowelList += (vowel + ",")
    #remove redundant vowels
    #remove ending comma
    vowelList = vowelList[:-1]
    words = vowelList.split(',')
    vowelList = ",".join(sorted(set(words), key=words.index))
    #get the meaning
    meaning = r.get_random_word()
      
    wordXml = gfg.Element("Word")
    root.append(wordXml)
      
    b1 = gfg.SubElement(wordXml, "Value")
    b1.text = word
    b2 = gfg.SubElement(wordXml, "Vowels")
    b2.text = vowelList
    b2 = gfg.SubElement(wordXml, "Meaning")
    b2.text = meaning
   
#tree = gfg.ElementTree(root)  

xmlstr = minidom.parseString(gfg.tostring(root)).toprettyxml(indent="   ")
with open(args.FileName, "w") as f:
    f.write(xmlstr)
