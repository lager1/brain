#!/opt/python3.3/bin/python3.3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# import knihoven
# ------------------------------------------------------------------------------
import os
import sys

# ------------------------------------------------------------------------------
class BrainFuck:
  """Interpretr jazyka brainfuck."""

  def __init__(self, data, memory = b'\x00', memory_pointer = 0):
    """Inicializace interpretru brainfucku."""

    # data programu
    self.data = data

    # inicializace proměnných
    #self.memory = bytearray(memory)

    # predelame na list -> nevyhazuje vyjimku s hodnotami !
    self.memory = list(memory)
    # zde priradit bytearray misto v hlavicce
    self.memory_pointer = memory_pointer

    # DEBUG a testy
    # a) paměť výstupu
    self.output = ''
    self.user_input = ''
    #self.brackets = []  # prazdny seznam zavorek
    self.brackets = dict()  # dict - zavorky

#self.memory_size = 0
# -> neni treba

    self.dataCheck()
    self.getInput()
    self.stripData()
    self.analyze()

    # tady pridame jeste neco jako 
    # vytvoreni seznamu -> klic, hodnota, klic je pozice leve zavorky, hodnota je pozice prave zavorky -> dict
    # nebo by byla moznost to udelat jako seznam dvojic -> leva a prava

    # debug
    #print(self.brackets)

    self.loop(0, len(self.data))



  # lepsi by asi bylo predelat data na seznam -> vyresi se modulo

  # pridat funkci pro ocisteni kodu od komentaru ?
  # -> urcite ma smysl ==> dobra optimalizace, protoze se musime vracet v kodu


  # dale ma smysl optimalizovat pomci spojovani stejnych prikazu zasebou -> napr 30 x + muzu vykonat jako jeden prikaz a nemusis 30 x iterovat

  # odevzdani v podstate do konce semestru


  # pridat odchyceni vyjimky bytearray index out of range ?
  # --> pridat kontrolu preteceni a podteceni

  #
  # pro potřeby testů
  #
  def get_memory(self):
    # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
    return self.memory

# ------------------------------------------------------------------------------
  def analyze(self):
    """Analyza dat - zpracovani smycek a ulozeni jejich pozic do dictu"""

# zde predpokladame pouze syntakticky spravne soubory -> stejny pocet zavorek [ a ]

    for (i, j) in enumerate(self.data):
      if j == "[":
        for (k, l) in enumerate(self.data[i:]):
          if l == "]":
            break

        self.brackets[i] = k + i


## ------------------------------------------------------------------------------
#  def analyze(self):
#    """Analyza dat - zpracovani smycek a ulozeni jejich pozic do seznamu"""
#
## zde predpokladame pouze syntakticky spravne soubory -> stejny pocet zavorek [ a ]
#
#    for (i, j) in enumerate(self.data):
#      if j == "[":
#        tmp = []
#        tmp.append(i)
#        for (k, l) in enumerate(self.data[i:]):
#          if l == "]":
#            break
#
#        tmp.append(k + i)
#        self.brackets.append(tmp)
#

# ------------------------------------------------------------------------------
  def stripData(self):
    """Orerazani dat o komentare"""

    tmpdata = ""

    for i in self.data:
      if i in "<>+-.,[]":
        tmpdata += i

    self.data = tmpdata

# ------------------------------------------------------------------------------
  def getInput(self):
    """Zpracovani potencialniho vstupu programu"""
    for (i, j) in enumerate(self.data):
      if self.data[i] == '!':
        self.user_input = self.data[(i + 1):]
        self.data = self.data[0:i]
        return

# pripadne dalsi vykricniky jsou soucasti vstupu

# ------------------------------------------------------------------------------
  def dataCheck(self):
    """Kontrola spravne zadaneho souboru s daty nebo spravneho kodu primo na radce"""

    if os.path.exists(self.data) and os.path.isfile(self.data):   # soubor existuje
      with open(self.data, 'r') as f:
        self.data = f.read()

    elif self.data == '.' or self.data == '..':                   # aktualni nebo nadrazeny adresar
      return


    # tohle v podstate asi ani neni potreba -> pouze privetivost pro uzivatele, navic v kodu muzou byt libovolne znaky 

    #elif not os.path.exists(self.data):
    #  for i in self.data:
    #    if i not in "<>+-.,[]!\n\r":     # kontrola zda se sklada pouze z dovolenych znaku - pozor, navic jeste \n, \r

    #    # debug
    #      print("i, ktere neni spravny znak: " + i + str(ord(i)))

    #      sys.exit("zadany soubor \"" + self.data + "\" neexistuje")

    #      # tady by to chtelo jeste predelat -> kod muze obsahovat i komentare !!!

    #elif not os.path.isfile(self.data):
    #  sys.exit("zadany soubor \"" + self.data + "\" neni soubor")
# ------------------------------------------------------------------------------
  def loop(self, start, end):
    """Vlastni smycka pro zpracovani kodu
       promenne:
         start   - kde smycka zacina
         end     - kde smycka konci
         pointer - pametove misto, ktere udava zda se ma smycka jeste provadet
    """


    i = start
    while i < end:

      #print("delka pameti: " + str(len(self.memory)))
      #print("pamet: " + str(self.memory))
      #print("aktualni index: " + str(i))
      #print("aktualni znak: " + self.data[i])
      #print("ukazatel: " + str(self.memory_pointer))
      #print("----------------")



      #print(str(len(self.memory)))
      #print(str(self.memory))
      #print(str(i))
      #print(self.data[i])
      #print(self.memory_pointer)
      #print("----------------")


# -----------------------------------
      if self.data[i] == '>':
        self.memory_pointer += 1
        if self.memory_pointer == len(self.memory):
      ##    print("pridavam pamet")
          self.memory.append(0)   # rozsireni pameti
      #  i += 1

      #  while self.data[i] == '>':
      #    self.memory_pointer += 1
      #    if self.memory_pointer == len(self.memory):
      # #     print("pridavam pamet")
      #      self.memory.append(0)   # rozsireni pameti
      #    i += 1
      #  continue

# -----------------------------------
      elif self.data[i] == '<':
        if self.memory_pointer != 0:
          self.memory_pointer -= 1
        i += 1

        #while self.data[i] == '<':
        #  self.memory_pointer -= 1
        #  i += 1


        # hm ?
        #if self.memory_pointer < 0:
        #  self.memory_pointer = 0

        continue

        # tady dodelat kontrolu ze nelze jit doleva, pokud jsme na zacatku pasky
        # asi neni vylozene nutne

# -----------------------------------
      elif self.data[i] == '+':
        self.memory[self.memory_pointer] += 1   # inkrementace aktualni pametove bunky
        #i += 1

        #while self.data[i] == '+':
        #  self.memory[self.memory_pointer] += 1   # inkrementace aktualni pametove bunky
        #  i += 1

        #self.memory[self.memory_pointer] %= 255
        #continue

# -----------------------------------
      elif self.data[i] == '-':
        self.memory[self.memory_pointer] -= 1   # dekrementace aktualni pametove bunky
        #i += 1

        #while self.data[i] == '-':
        #  self.memory[self.memory_pointer] -= 1   # inkrementace aktualni pametove bunky
        #  i += 1

        #self.memory[self.memory_pointer] %= 255
        #continue

# -----------------------------------
      elif self.data[i] == '.':
        #self.output = self.memory.decode("utf-8")[self.memory_pointer]
        #self.output = chr(self.memory[self.memory_pointer])
        #self.output = self.output + chr(self.memory[self.memory_pointer])
        # hm ?


        self.output = self.output + chr(self.memory[self.memory_pointer])
        print(chr(self.memory[self.memory_pointer]), end="")
        sys.stdout.flush()


        #print(self.output, end="")
        #sys.stdout.flush()

# -----------------------------------
      elif self.data[i] == ',':
        if self.user_input != "":
          self.memory[self.memory_pointer] = ord(self.user_input[0])
          self.user_input = self.user_input[1:]

        else:
          self.memory[self.memory_pointer] = ord(sys.stdin.read(1))

# -----------------------------------
      elif self.data[i] == '[':
        if self.memory[self.memory_pointer] == 0:
          i = self.brackets.get(i) + 1  # skok na znak za koncem cyklu
          continue

        else:
          i = self.loop(i + 1, len(self.data))     # len(self.data) neni nejlepsi - dalo by se vylepsit

# -----------------------------------
      elif self.data[i] == ']':

        if self.memory[self.memory_pointer] == 0:
          return (i)    # vracime pozici, na kterou se ma skocit

        else:
          i = start                        # skok na zacatek cyklu
          continue

      i += 1
# -----------------------------------
    # nakonec musime vratit bytearray
    self.memory = bytearray(self.memory)

    #print(self.output, end="")
    #sys.stdout.flush()
    # toto je nesmysl

    # na konci implicitne tisk ?

# ------------------------------------------------------------------------------
class BrainLxoller():
  """Třída pro zpracování jazyka brainloller."""


  def __init__(self, filename):
    """Inicializace interpretru brainlolleru."""


    # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
    self.data = ''
    # ..který pak předhodíme interpretru
    self.program = BrainFuck(self.data)

# ------------------------------------------------------------------------------
class BrainCopter():
  """Třída pro zpracování jazyka braincopter."""


  def __init__(self, filename):
    """Inicializace interpretru braincopteru."""

    # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
    self.data = self.convert(filename)
    # ..který pak předhodíme interpretru
    self.program = BrainFuck(self.data)


# ------------------------------------------------------------------------------
  def convert(self, filename):
    """funkce pro konverzi brainCopteru na brainfuck"""

    with open(filename) as f:
      data = f.read()

    print(data)


