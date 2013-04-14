#!/opt/python3.3/bin/python3.3
# -*- coding: utf-8 -*-


# ------------------------------------------------------------------------------
# import knihoven
# ------------------------------------------------------------------------------
import os
import sys
import struct

# ------------------------------------------------------------------------------
class BrainFuck:
  """Interpretr jazyka brainfuck."""

  #def __init__(self, data, memory = b'\x00', memory_pointer = 0):
  def __init__(self, data, memory = bytearray(b'\x00'), memory_pointer = 0):
    """Inicializace interpretru brainfucku."""

    # data programu
    self.data = data

    # inicializace proměnných
    self.memory = memory
    self.memory_pointer = memory_pointer


    # DEBUG a testy
    # a) paměť výstupu
    self.output = ''

    self.dataCheck()
    #self.loop(0, len(self.data))
    self.loop(0, len(self.data) - 1)

  # pridat funkci pro ocisteni kodu od komentaru ?
  # pridat odchyceni vyjimky bytearray index out of range ?

  #
  # pro potřeby testů
  #
  def get_memory(self):
    # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
    return self.memory

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

    elif not os.path.isfile(self.data):
      sys.exit("zadany soubor \"" + self.data + "\" neni soubor")
# ------------------------------------------------------------------------------
  #def loop(self, start = 0, end = len(self.data)):
  #def loop(self, start, end, pointer):
  def loop(self, start, end):
    """Vlastni smycka pro zpracovani kodu
       promenne:
         start   - kde smycka zacina
         end     - kde smycka konci
         pointer - pametove misto, ktere udava zda se ma smycka jeste provadet
    """


   # for (i, j) in enumerate(self.data):
   #   print(i, j)


    #print("-----------------------------------")
    #print("start " + str(start))
    #print("end " + str(end))

    i = start
    while i < end:

      #print(i, self.data[i])
      #print("ukazatel " + str(self.memory_pointer))
      #print("pamet " + str(self.memory[self.memory_pointer]))

      if self.data[i] == '>':
        self.memory_pointer += 1
        self.memory.append(0)   # rozsireni pameti

      elif self.data[i] == '<':
        self.memory_pointer -= 1

      elif self.data[i] == '+':
        self.memory[self.memory_pointer] += 1

      elif self.data[i] == '-':
        self.memory[self.memory_pointer] -= 1

      elif self.data[i] == '.':
        self.output = self.memory.decode("utf-8")[self.memory_pointer]
        print(self.output, end="")

      elif self.data[i] == ',':
        pass
        # cteni vstupu

      elif self.data[i] == '[':

        for (k, l) in enumerate(self.data):
          if l == ']':
            self.loop(i + 1, k + 1)   # jdeme na znak za zacatkem cyklu, jinak se zacyklime, chceme ukoncovaci zavorku
            break
        #print("k je " + str(k))
        i = k + 1                # skok za konec smycky
        continue

      elif self.data[i] == ']':
        if self.memory[self.memory_pointer] == 0:
          #print("pamet je 0, koncime cyklus")
          return

        else:
        #  print("pamet neni 0")
          self.memory[self.memory_pointer] -= 1

        #  print("ukazatel nastaven " + str(self.memory_pointer))
        #  print("pamet " + str(self.memory[self.memory_pointer]))

          i = start                        # skok na zacatek cyklu
          continue

      elif self.data[i] == '!':
        pass

      i += 1

# ------------------------------------------------------------------------------
class BrainLoller():
  """Třída pro zpracování jazyka brainloller."""


  def __init__(self, filename):
    """Inicializace interpretru brainlolleru."""


    # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
    self.data = ''
    # ..který pak předhodíme interpretru
    self.program = BrainFuck(self.data)


class BrainCopter():
  """Třída pro zpracování jazyka braincopter."""


  def __init__(self, filename):
    """Inicializace interpretru braincopteru."""


    # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
    self.data = ''
    # ..který pak předhodíme interpretru
    self.program = BrainFuck(self.data)


