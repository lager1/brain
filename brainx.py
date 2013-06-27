#!/opt/python3.3/bin/python3.3
# encoding: utf-8

# ------------------------------------------------------------------------------
import os
import sys
import image_png
import struct

# ------------------------------------------------------------------------------
class BrainFuck:
    """Interpretr jazyka brainfuck."""

    def __init__(self, data, memory = b'\x00', memory_pointer = 0):
        """Inicializace interpretru brainfucku."""

        # data programu
        self.data = data

        # inicializace proměnných
        self.memory = list(memory)
        self.memory_pointer = memory_pointer

        # DEBUG a testy
        # a) paměť výstupu
        # a) paměť vstupu
        self.output = ''
        self.user_input = ''

        self.brackets = dict()  # dict - zavorky

        self.dataCheck()
        self.getInput()
        self.stripData()
        self.analyze(0)
        self.loop(0, len(self.data))

      #
      # pro potřeby testů
      #
      def get_memory(self):
          # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
          return bytearray(self.memory) # vracime bytearray


# ------------------------------------------------------------------------------
    def analyze(self, start):
        """Analyza dat - zpracovani smycek a ulozeni jejich pozic do dictu
        parametr start udava odkud zaciname hledat
        """

        # zde predpokladame pouze syntakticky spravne soubory -> stejny pocet zavorek [ a ]

        delka = len(self.data)
        i = start

        while i < delka:

            if self.data[i] == "[":
                i = self.analyze(i + 1) + 1    # posuneme hledani za nalezenou zavorku
                continue

              if i >= delka:
                return delka

            if self.data[i] == "]":
                self.brackets[start - 1] = i
                return i

            i += 1

        return delka

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
        # pripadne dalsi vykricniky jsou soucasti vstupu

        for (i, j) in enumerate(self.data):
            if self.data[i] == '!':
                self.user_input = self.data[(i + 1):]
                self.data = self.data[0:i]
                return

# ------------------------------------------------------------------------------
    def dataCheck(self):
        """Kontrola spravne zadaneho souboru s daty nebo spravneho kodu primo na radce"""

        if os.path.exists(self.data) and os.path.isfile(self.data):   # soubor existuje
            with open(self.data, 'r') as f:
                self.data = f.read()

        elif self.data == '.' or self.data == '..':                   # aktualni nebo nadrazeny adresar
            return

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

# -----------------------------------
            if self.data[i] == '>':
                self.memory_pointer += 1
                if self.memory_pointer == len(self.memory):
                    self.memory.append(0)   # rozsireni pameti
                i += 1

                while self.data[i] == '>':
                    self.memory_pointer += 1
                    if self.memory_pointer == len(self.memory):
                        self.memory.append(0)   # rozsireni pameti
                    i += 1
                continue

# -----------------------------------
            elif self.data[i] == '<':
                if self.memory_pointer != 0:
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
                self.memory[self.memory_pointer] += 1   # inkrementace aktualni pametove bunky
                i += 1

                while self.data[i] == '+':
                    self.memory[self.memory_pointer] += 1   # inkrementace aktualni pametove bunky
                    i += 1

                self.memory[self.memory_pointer] %= 255
                continue

# -----------------------------------
            elif self.data[i] == '-':
                self.memory[self.memory_pointer] -= 1   # dekrementace aktualni pametove bunky
                i += 1

                while self.data[i] == '-':
                    self.memory[self.memory_pointer] -= 1   # inkrementace aktualni pametove bunky
                    i += 1

                self.memory[self.memory_pointer] %= 255
                continue

# -----------------------------------
            elif self.data[i] == '.':
                self.output = self.output + chr(self.memory[self.memory_pointer])
                print(chr(self.memory[self.memory_pointer]), end="")
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

# ------------------------------------------------------------------------------
class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""


    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""

        self.raw_data = image_png.PngReader(filename)

        # smery:
        # 0 - vlevo
        # 1 - dolu
        # 2 - vpravo
        # 3 - nahoru

        self.direction = 0
        self.pos_x = 0
        self.pos_y = 0

        print(self.raw_data.rgb)


        # debug
        #return

        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''

        while self.pos_x < struct.unpack('>I', self.raw_data.ihdr_width)[0] and self.pos_y < struct.unpack('>I', self.raw_data.ihdr_height)[0]:

            print(self.raw_data.rgb[self.pos_y][self.pos_x])
            print(self.data)
            #print("pozice y: " + str(self.pos_y))
            #print("pozice x: " + str(self.pos_x))

            if self.raw_data.rgb[self.pos_y][self.pos_x] == (255, 0, 0):
                self.data += '>'

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (128, 0, 0):
                self.data += '<'

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (0, 255, 0):
                self.data += '+'

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (0, 128, 0):
                self.data += '-'
            #  print("tady")
              # debug
            #  if self.pos_x > 10:
            #    return

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (0, 0, 255):
                self.data += '.'

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (0, 0, 128):
                self.data += ','

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (255, 255, 0):
                self.data += '['

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (128, 128, 0):
                self.data += ']'

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (0, 255, 255):
                print("vpravo")
                self.direction += 1     # otoceni doprava
                self.direction %= 4

            elif self.raw_data.rgb[self.pos_y][self.pos_x] == (0, 128, 128):
                print("vlevo")
                self.direction -= 1     # otoceni doleva
                self.direction %= 4

            if self.direction == 0:
                self.pos_x += 1

            elif self.direction == 1:
                self.pos_y += 1

            elif self.direction == 2:
                self.pos_x -= 1

            elif self.direction == 3:
                self.pos_y -= 1

        print(self.data)

        ## ..který pak předhodíme interpretru
        #self.program = BrainFuck(self.data)

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

        self.raw_data = image_png.PngReader(filename)

        # smery:
        # 0 - vlevo
        # 1 - dolu
        # 2 - vpravo
        # 3 - nahoru

        self.direction = 0
        self.pos_x = 0
        self.pos_y = 0

        self.converted = []

        for i in self.raw_data.rgb:
            self.tmp = []
            for r, g, b in i:
                self.tmp.append((65536 * r + 256 * g + b) % 11) # prevod na prikazy

          self.converted.append(self.tmp)

        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''

        while self.pos_x < struct.unpack('>I', self.raw_data.ihdr_width)[0] and self.pos_y < struct.unpack('>I', self.raw_data.ihdr_height)[0]:

            if self.converted[self.pos_y][self.pos_x] == 0:
                self.data += '>'

            elif self.converted[self.pos_y][self.pos_x] == 1:
                self.data += '<'

            elif self.converted[self.pos_y][self.pos_x] == 2:
                self.data += '+'

            elif self.converted[self.pos_y][self.pos_x] == 3:
                self.data += '-'

            elif self.converted[self.pos_y][self.pos_x] == 4:
                self.data += '.'

            elif self.converted[self.pos_y][self.pos_x] == 5:
                self.data += ','

            elif self.converted[self.pos_y][self.pos_x] == 6:
                self.data += '['

            elif self.converted[self.pos_y][self.pos_x] == 7:
                self.data += ']'

            elif self.converted[self.pos_y][self.pos_x] == 8:
                self.direction += 1     # otoceni doprava
                self.direction %= 4

            elif self.converted[self.pos_y][self.pos_x] == 9:
                self.direction -= 1     # otoceni doleva
                self.direction %= 4

            if self.direction == 0:
                self.pos_x += 1

            elif self.direction == 1:
                self.pos_y += 1

            elif self.direction == 2:
                self.pos_x -= 1

            elif self.direction == 3:
                self.pos_y -= 1

        return self.data

