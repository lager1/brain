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
    self.memory = bytearray(memory)
    # zde priradit bytearray misto v hlavicce
    self.memory_pointer = memory_pointer

    # DEBUG a testy
    # a) paměť výstupu
    self.output = ''
    self.user_input = ''
    self.memory_size = 0

    self.dataCheck()
    self.getInput()
    self.stripData()
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

    elif not os.path.exists(self.data):
      for i in self.data:
        if i not in "<>+-.,[]!":     # kontrola zda se sklada pouze z dovolenych znaku
          sys.exit("zadany soubor \"" + self.data + "\" neexistuje")

          # tady by to chtelo jeste predelat -> kod muze obsahovat i komentare !!!

    elif not os.path.isfile(self.data):
      sys.exit("zadany soubor \"" + self.data + "\" neni soubor")
# ------------------------------------------------------------------------------
  def loop(self, start, end):
    """Vlastni smycka pro zpracovani kodu
       promenne:
         start   - kde smycka zacina
         end     - kde smycka konci
         pointer - pametove misto, ktere udava zda se ma smycka jeste provadet
    """

    #print("============================")

    i = start
    while i < end:

      # debug
      #print(self.memory)
      #print(i, self.data[i])


# -----------------------------------
      if self.data[i] == '>':
        self.memory_pointer += 1
        if self.memory_pointer == len(self.memory):
          self.memory.append(0)   # rozsireni pameti

    #i += 1

    #    while self.data[i] == '>':
    #      self.memory_pointer += 1
    #      if self.memory_pointer == len(self.memory):
    #        self.memory.append(0)   # rozsireni pameti
    #      i += 1
    #    continue

# -----------------------------------
      elif self.data[i] == '<':
        self.memory_pointer -= 1
        i += 1

        while self.data[i] == '<':
          self.memory_pointer -= 1
          i += 1
        continue

        # tady dodelat kontrolu ze nelze jit doleva, pokud jsme na zacatku pasky
        # asi neni vylozene nutne

# -----------------------------------
      elif self.data[i] == '+':
        if int(self.memory[self.memory_pointer]) + 1 >= 256:
          self.memory[self.memory_pointer] %= 255
        self.memory[self.memory_pointer] += 1   # inkrementace aktualni pametove bunky
        i += 1

        while self.data[i] == '+':
          #print(self.memory[self.memory_pointer])
          if int(self.memory[self.memory_pointer]) + 1 >= 256:
            self.memory[self.memory_pointer] %= 255
          self.memory[self.memory_pointer] += 1   # inkrementace aktualni pametove bunky
          i += 1

        continue

# -----------------------------------
      elif self.data[i] == '-':
        self.memory[self.memory_pointer] -= 1   # dekrementace aktualni pametove bunky
        i += 1

        while self.data[i] == '-':
          self.memory[self.memory_pointer] -= 1   # inkrementace aktualni pametove bunky
          i += 1
        continue

# -----------------------------------
      elif self.data[i] == '.':
        #self.output = self.memory.decode("utf-8")[self.memory_pointer]
        self.output = chr(self.memory[self.memory_pointer])

        print(self.output, end="")
        sys.stdout.flush()

# -----------------------------------
      elif self.data[i] == ',':
        if self.user_input != "":
          self.memory[self.memory_pointer] = ord(self.user_input[0])
          self.user_input = self.user_input[1:]

        else:
          self.memory[self.memory_pointer] = ord(sys.stdin.read(1))

# -----------------------------------
      elif self.data[i] == '[':
        i = self.loop(i + 1, len(self.data))     # len(self.data) neni nejlepsi - dalo by se vylepsit

        #i = k + 1                # skok za konec smycky


      #  #for (k, l) in enumerate(self.data):
      #  for (k, l) in enumerate(self.data[(i + 1):]):     # vylepseni -> musime hledat od soucasne pozice dale, jinak mame problem !
      #    # debug
      #    print("cyklus, k: " + str(k) + ", l " + str(l))

      #    if l == ']':
      #      # debug
      #      print("podminka ", i, k)

      #      self.loop(i + 1, k + 1)   # jdeme na znak za zacatkem cyklu, jinak se zacyklime, chceme ukoncovaci zavorku
      #      break

      #  i = k + 1                # skok za konec smycky
      #  continue

# -----------------------------------
      elif self.data[i] == ']':

        if self.memory[self.memory_pointer] == 0:

          # debug
          #print("=============RET============")

          #return (i + 1)    # vracime pozici, na kterou se ma skocit
          return (i)    # vracime pozici, na kterou se ma skocit

        else:
          i = start                        # skok na zacatek cyklu
          continue

      i += 1

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






