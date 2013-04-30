#!/opt/python3.3/bin/python3.3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# import knihoven
# ------------------------------------------------------------------------------
import os
import sys
import struct
import subprocess

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

    self.dataCheck()
    #self.getInput()
    self.stripData()
    self.loop(0, len(self.data))


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
    """Orerazani dat o komentare a pripadny vstup pro vlastni program"""

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
        p = subprocess.Popen(os.getpid(), stdin = subprocess.PIPE)
        p.communicate(input = self.data[(i + 1):])
#        sys.stdin.write(self.data[i:])
#
# import subprocess
# p = subprocess.Popen(['bla'], stdin=subprocess.PIPE)
# p.communicate(input = "blabalbal")
#

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

    i = start
    while i < end:

      if self.data[i] == '>':
        self.memory_pointer += 1
        self.memory.append(0)   # rozsireni pameti

      elif self.data[i] == '<':
        self.memory_pointer -= 1

        # tadyo dodelat kontrolu ze nelze jit doleva, pokud jsme na zacatku pasky

      elif self.data[i] == '+':
        self.memory[self.memory_pointer] += 1   # inkrementace aktualni pametove bunky

      elif self.data[i] == '-':
        self.memory[self.memory_pointer] -= 1   # dekrementace aktualni pametove bunky

      elif self.data[i] == '.':
        self.output = self.memory.decode("utf-8")[self.memory_pointer]
        print(self.output, end="")
        sys.stdout.flush()

      elif self.data[i] == ',':
        self.memory[self.memory_pointer] = ord(sys.stdin.read(1))

      elif self.data[i] == '[':

        for (k, l) in enumerate(self.data):
          if l == ']':
            self.loop(i + 1, k + 1)   # jdeme na znak za zacatkem cyklu, jinak se zacyklime, chceme ukoncovaci zavorku
            break

        i = k + 1                # skok za konec smycky
        continue

      elif self.data[i] == ']':

        if self.memory[self.memory_pointer] == 0:
          return

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
    self.data = ''
    # ..který pak předhodíme interpretru
    self.program = BrainFuck(self.data)


