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
    self.memory = memory
    self.memory_pointer = memory_pointer


    # DEBUG a testy
    # a) paměť výstupu
    self.output = ''

    self.dataCheck()
    self.loop()

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
  def loop(self):
    """Vlastni smycka pro zpracovani kodu"""

    for i in self.data:
      if i == '>':
        self.memory_pointer += 1
        # pridat jeste rozsireni pameti

      elif i == '<':
        self.memory_pointer -= 1
        # pridat jeste rozsireni pameti

      elif i == '+':
        self.memory += 1

      elif i == '':
        self.memory -= 1

      elif i == '.':
        print(self.memory)

      elif i == ',':
        pass
        # cteni vstupu

      elif i == '[':
        pass

      elif i == ']':
        pass

      elif i == '!':
        pass



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


