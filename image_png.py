#!/opt/python3.3/bin/python3.3
# encoding: utf-8

import struct
import zlib

class PNGWrongHeaderError(Exception):
    """Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""

    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)

class PNGNotImplementedError(Exception):
    """Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""

    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)


class PNGWrongCrcError(Exception):
    """Výjimka oznamující, že PNG-obrázek je poškozen."""

    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)


class PngReader():
    """Třída pro práci s PNG-obrázky."""


    def paeth(self, a, b, c):       # filtr 4
      p = a + b - c
      pa = abs(p - a)
      pb = abs(p - b)
      pc = abs(p - c)

      if pa <= pb and pa <= pc:
        return a

      elif pb <= pc:
        return b

      else:
        return c

    def __init__(self, filepath):

      # RGB-data obrázku jako seznam seznamů řádek,
      #   v každé řádce co pixel, to trojce (R, G, B)
      self.rgb = []
      self.pix = []     # pouze pixely - pomocna promenna

      with open(filepath, 'rb') as f:
        self.header = f.read(8)

        if self.header != b'\x89PNG\r\n\x1a\n':
          raise PNGWrongHeaderError("Hlavička zadaného souboru neodpovídá formátu PNG.")

        self.ihdr_len = f.read(4)    # delka chunku
        self.ihdr_type = f.read(4)   # typ chunku

        if self.ihdr_type != b'IHDR':
          raise PNGNotImplementedError("Strukturu zadaného souboru není možné zpracovat.")

        self.ihdr_data = f.read(13)  # 13 bajtu dat

        self.ihdr_width = self.ihdr_data[:4]  # vyska obrazku v pixelech
        self.ihdr_height = self.ihdr_data[4:8] # sirka obrazku v pixelech
        self.ihdr_depth = self.ihdr_data[8:9]  # bitova hloubka
        self.ihdr_col_type = self.ihdr_data[9:10]   # barvovy typ
        self.ihdr_compression = self.ihdr_data[10:11]   # metoda komprese
        self.ihdr_filter = self.ihdr_data[11:12]        # metoda filtrace
        self.ihdr_interlace = self.ihdr_data[12:13]     # metoda prokladani , musi byt 0 !

        self.ihdr_crc = f.read(4)     # kontrolni soucet

        if zlib.crc32(self.ihdr_type + self.ihdr_data) != struct.unpack('>I', self.ihdr_crc)[0]:
          raise PNGWrongCrcError("Zadaný soubor je pravděpodobně poškozen.")

        self.chunk_len = f.read(4)
        self.idat = b''

        while self.chunk_len != b'\x00\x00\x00\x00':     # cteni vseho az do IEND
          self.chunk_type = f.read(4)    # typ chunku

          if self.chunk_type != b'IDAT':
            raise PNGNotImplementedError("Strukturu zadaného souboru není možné zpracovat.")

          self.chunk_data = f.read(struct.unpack('>I', self.chunk_len)[0])  # precteni vsech dat chunku
          self.idat += self.chunk_data
          self.chunk_crc = f.read(4)

          if zlib.crc32(self.chunk_type + self.chunk_data) != struct.unpack('>I', self.chunk_crc)[0]:
            raise PNGWrongCrcError("Zadaný soubor je pravděpodobně poškozen.")

          self.chunk_len = f.read(4)

        self.iend_len = self.chunk_len
        self.iend_type = f.read(4)   # typ
        self.iend_crc = f.read(4)   # crc

        if zlib.crc32(self.iend_type) != struct.unpack('>I', self.iend_crc)[0]:
          raise PNGWrongCrcError("Zadaný soubor je pravděpodobně poškozen.")

        self.data = zlib.decompress(self.idat)

        for i in range(0, len(self.data), (struct.unpack('>I', self.ihdr_width)[0] * 3) + 1):  # cyklus pro pocet radek s krokem sirky radku + 1
          self.scanline = [self.data[i]]

          self.tmp = []
          for j in range(1, struct.unpack('>I', self.ihdr_width)[0] * 3, 3):   # cyklus pro jednotlive pixely v radku
            self.tmp.append(list(struct.unpack('>BBB', self.data[i + j:i + j + 3])))

          self.scanline.append(self.tmp)
          self.rgb.append(self.scanline)

        print(self.rgb)
        print("")
        print("")

        # filtry jsou pro jednotlive scanlines

        for i in range(struct.unpack('>I', self.ihdr_height)[0]):  # cyklus pro pocet radek -> zpracovani filtru
          if self.rgb[i][0] == 0:
            self.pix.append(self.rgb[i][1])     # pridame do vysledku radek bez filtru

          elif self.rgb[i][0] == 1:
            for j in range(struct.unpack('>I', self.ihdr_width)[0]):

              if j >= 1:
                for k in range(3):
                  self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + self.rgb[i][1][j - 1][k]) & 0xff)

            self.pix.append(self.rgb[i][1])    # pridame do vysledku radek bez filtru

          elif self.rgb[i][0] == 2:
            for j in range(struct.unpack('>I', self.ihdr_width)[0]):

              if i >= 1:
                for k in range(3):
                  self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + self.rgb[i - 1][1][j][k]) & 0xff)

            self.pix.append(self.rgb[i][1])    # pridame do vysledku radek bez filtru


            # POZOR !!!!! PROBLEM -> PRIRAZUJEME DO PIX, ALE STALE CTEME RGB !!
            # prirazujeme zaroven do rgb, pix je pouze kopie bez filtru
            # 
            # 

          elif self.rgb[i][0] == 3:
            for j in range(struct.unpack('>I', self.ihdr_width)[0]):

              if i < 1 and j < 1:
                pass

              elif i < 1:
                for k in range(3):
                  self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + (self.rgb[i][1][j - 1][k]) // 2) & 0xff)

              elif j < 1:
                for k in range(3):
                  self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + (self.rgb[i - 1][1][j][k]) // 2) & 0xff)

              else:
                for k in range(3):
                  self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + (self.rgb[i - 1][1][j][k] + self.rgb[i - 1][1][j][k]) // 2) & 0xff)


            self.pix.append(self.rgb[i][1])    # pridame do vysledku radek bez filtru


          elif self.rgb[i][0] == 4:
            for j in range(struct.unpack('>I', self.ihdr_width)[0]):

              for k in range(3):
                self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + self.paeth(self.rgb[i][1][j - 1][k], self.rgb[i - 1][1][j][k], self.rgb[i - 1][1][j - 1][k])) & 0xff)

            self.pix.append(self.rgb[i][1])    # pridame do vysledku radek bez filtru


         # elif self.rgb[i][0] == 4:
         #   for j in range(struct.unpack('>I', self.ihdr_width)[0]):
         #     self.rgb_cpy[i][1][j].clear() # vycisteni pixelu, ktery zpracujeme

         #     for k in range(3):
         #       self.rgb_cpy[i][1][j].append((self.rgb[i][1][j][k] + self.paeth(self.rgb[i][1][j - 1][k], self.rgb[i - 1][1][j][k], self.rgb[i - 1][1][j - 1][k])) & 0xff)


         #   self.pix.append(self.rgb_cpy[i][1])    # pridame do vysledku radek bez filtru
         #   self.rgb = copy.deepcopy(self.rgb_cpy)




          #  # je treba pixely prochazet na urovni bajtu !!!!
          #  #for k in range(struct.unpack('>I', self.ihdr_height)[0]):
          #  for l in range(struct.unpack('>I', self.ihdr_width)[0]):      # mozna nutnost osetreni neexistence .. ?
          #    #self.rgb_cpy[i][1][l].clear()   # vycistime vsechny docasne pixely
          #    for m in range(3):
          #      print(self.rgb[i][1][l][m])
          #      #print(self.rgb[i][1][l][m] + self.paeth(self.rgb[i][1][l - 1][m], self.rgb[i - 1][1][l][m], self.rgb[i - 1][1][l - 1][m]))

          #      self.rgb_cpy[i][1][l].append(self.rgb[i][1][l][m] + self.paeth(self.rgb[i][1][l - 1][m], self.rgb[i - 1][1][l][m], self.rgb[i - 1][1][l - 1][m]))    # pixely jsou az o uroven niz !!
          #    # po rozfiltrovani jednoho pixelu zkopirovat jednu mapu na druhou?
          #    #self.rgb = copy.deepcopy(self.rgb_cpy)
          #    self.rgb = copy.deepcopy(self.rgb_cpy)
          #  print(self.rgb_cpy)
          #  print("")
          #  print("")
          #  print("")
          #  print("")
          #  print("")
          #  print("")
          #  print("")
          #  print(self.rgb)
          #  return

        self.rgb = []
        # konverze na trojice rgb hodnot
        for i in self.pix:
          self.tmp = []
          for j in i:
            self.tmp.append(tuple(j))
          self.rgb.append(self.tmp)


        print(self.rgb)
        print("")
        print("")
        print("")
        print(self.pix)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------



            # projiti vsech pixelu obrazku:
            #for k in range(struct.unpack('>I', self.ihdr_height)[0]):
            #  print("[", end='')
            #  for l in range(struct.unpack('>I', self.ihdr_width)[0]):
            #    print(self.rgb[k][1][l], end=', ')
            #  print("]")




# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

        #i = 0
        #tmp = []
        #while i < len(self.data):

        #  if i % ((struct.unpack('>I', self.ihdr_width)[0] * 3) + 1) == 0:
        #    tmp = []

        #    print("filtr")
        #    print(self.data[i])

        #    if self.data[i] == 0:
        #      i += 1
        #      continue

        #    elif self.data[i] == 1:
        #      pass

        #    elif self.data[i] == 2:
        #      pass

        #    elif self.data[i] == 3:
        #      pass

        #    elif self.data[i] == 4:
        #      for k in range(struct.unpack('>I', self.ihdr_height)[0]):
        #        for l in range(struct.unpack('>I', self.ihdr_width)[0]):
        #          self.data[k][l] = self.data[k][l] - paeth(self.data[k - 1][l], self.data[k][l - 1], self.data[k - 1][l - 1])

        #    i += 1
        #      #pass


        #  for j in range(0, struct.unpack('>I', self.ihdr_width)[0] * 3, 3):
        ##    print(self.data[i + j: i + j + 3])
        #    tmp.append(struct.unpack('>BBB', self.data[i + j: i + j + 3]))

        ##  print("j: " + str(j))
        ##  print("i: " + str(i))
        #  i += j + 3

        #  self.rgb.append(tmp)
        #  #i += 1

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


        #print(struct.unpack('>I', self.ihdr_width)[0])
        #print(struct.unpack('>I', self.ihdr_height)[0])
        #print(self.data)

        #for i in range(struct.unpack('>I', self.ihdr_width)[0]):
        #  for j in range(struct.unpack('>I', self.ihdr_height)[0]):
        #tmp = list()

        #for i in range((struct.unpack('>I', self.ihdr_width)[0] *  struct.unpack('>I', self.ihdr_width)[0] + 1) * 3, ):
        #  print()

          #if i % ((struct.unpack('>I', self.ihdr_width)[0] * 3) + 1) == 0:
          #  continue

          #tmp.append(self.data[i])
          #if len(tmp) == 3:
          #  print(tmp)
          #  tmp = []


        #for i in range(1, (struct.unpack('>I', self.ihdr_height)[0] * struct.unpack('>I', self.ihdr_width)[0] + 1) * 3, (struct.unpack('>I', self.ihdr_width)[0] * 3) + 1):
        #  self.tmp = []


        #  for j in range(0, 3 * struct.unpack('>I', self.ihdr_width)[0], 3):

        ##    print(self.data[i + j: i + j + 3])

        #    self.tmp.append(struct.unpack('>BBB', self.data[i + j:i + j + 3]))
        #  self.rgb.append(self.tmp)


        #print(self.rgb)


