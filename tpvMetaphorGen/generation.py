#coding:utf-8
import random
import re
import json
from googletrans import Translator

global dic
global ppCount
global adjCount
global prevChoix
global contextAdded
global derivation
global dic
global ppCount

def generatePreciado(elems, newdic):
  global ppCount
  l = []
  elems = re.split(" ", elems)
  for e in elems:
    if e in newdic:
      choix = re.split("\|", newdic[e])
      j = random.randrange(0, len(choix))

      if 'PP' in choix[j]:
        ppCount += 1
        if ppCount > 3:
          choix = ['NPsPP']
          j = 0

      l += generatePreciado(choix[j], newdic)
    else:
      l.append(e)
  return l

def preciadoGen():

  newdic = json.load(open("preciado.json"))

  StructPhrases = re.split("\|", newdic["S"])
  nbPhrases = 1
  for i in range(nbPhrases):
    ppCount = 0
    j = random.randrange(0, len(StructPhrases))
    chunks = StructPhrases[j]
    res = generatePreciado(chunks,newdic)
    print (" ".join(res))
    f = open("phrasesGen.txt", "a")
    f.write(" ".join(res))
    f.write('\n\n')
    f.close()
    
def extractContext(tokens):

  for token in tokens:
    if (token in dic['N'].split('|')) :
      return ['N',token]
    if (token in dic['NOMP'].split('|')) :
      return ['NOMP',token]

  return 'none'

def generate(elems,context):
  global ppCount
  global adjCount
  global prevChoix
  global vpCount
  global first
  global contextAdded
  global derivation
  prevChoix = ''


  l = []
  elems = re.split(" ", elems)#on découpe en symboles
  for e in elems:
    if e in dic:#on a un symbole non-terminal
      choix = re.split("\|", dic[e])#dans le Json les alternatives sont séparées par des "|" ou pipe
      j = random.randrange(0, len(choix))

      rand = random.randrange(0, 100)
      if rand % 2 == 0:
        while'PP' in choix[j]:
          j = random.randrange(0, len(choix))

      if first and 'PrP' in choix[j] :
        while'PrP' in choix[j]:
          j = random.randrange(0, len(choix))
        first = False

      if 'PP' in choix[j]:
        ppCount += 1
        if ppCount > 1:
          choix = ['NPsPP']
          j = 0

      if 'VP' in choix[j]:
        vpCount += 1
        if vpCount > 2:
          choix = ['V NP','IS ADJP','IS NP','V ADJP2']
          j = 0

      if 'ADJ' in choix[j] and prevChoix is 'NP':
        adjCount += 1
        if adjCount > 1:
          choix = ['NOMP','DET N','DET N PP','NOMP PP','pDET pN','pDET pN PP']
          j = random.randrange(0, len(choix))

      if e == 'NP' and context[0] is 'NOMP' and not contextAdded:
        choix = ['NOMP','DET ADJ NOMP PP','NOMP PP']
        j = random.randrange(0, len(choix))

      if e == 'NP'  and context[0] is 'N' and not contextAdded:
        while ('NOMP' in choix[j]) or ('pN' in choix[j]):
          j = random.randrange(0, len(choix))

      if e ==  'NOMP' and context[0] is 'NOMP' and not contextAdded:

        choix = [context[1]]
        j = 0
        contextAdded = True
        

      if e == 'N' and context[0] is 'N' and not contextAdded:
        choix = [context[1]]
        j= 0
        contextAdded = True

      prevChoix = choix[j]
      derivation.append(e)

      l += generate(choix[j], context)# on appelle récursivement la fonction
    else:#on a un symbole terminal
      l.append(e)
      derivation.append(e)
  return l



dic = json.load(open("JCVD.json"))#les règles de génération

StructPhrases = re.split("\|", dic["S"])#On fait une liste des phrases possibles

print(StructPhrases)
print('ask me some shit')
print('\n\n')

nbPhrases = 5
conversation = True

while conversation:

  contextTokens =  input()



  context = extractContext(contextTokens.split())

  for i in range(0, nbPhrases):

    ppCount = 0
    adjCount = 0
    vpCount = 0
    first = True
    contextAdded = False

    j = random.randrange(0, len(StructPhrases))
    chunks = StructPhrases[j]#on chosiit une structure de phrase au hasard
    derivation = []
    res = generate(chunks,context)
    textfinal = " ".join(res)
    translator = Translator()
    translation = translator.translate(textfinal,dest='fr').text

  
    if len(translation)< 60:
      print (translation)

    f = open("phrasesGen.txt", "a")
    f.write(" ".join(res))
    f.write('\n\n')
    f.close()

  print('\n\n')

  input()
  preciadoGen()


