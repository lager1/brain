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

    def __init__(self, filepath):

      self.rgb = []

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
        while self.chunk_len != b'\x00\x00\x00\x00':     # cteni vseho az do IEND

          self.chunk_type = f.read(4)    # typ chunku

          if self.chunk_type != b'IDAT':
            raise PNGNotImplementedError("Strukturu zadaného souboru není možné zpracovat.")

          self.idat = b''

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

        print("------------------------------------------------------")

        self.data = zlib.decompress(self.idat)
        print(self.data)
        #print(len(self.data))

        #for i in range((struct.unpack('>I', self.ihdr_height)[0] * struct.unpack('>I', self.ihdr_width)[0] + 1) * 3):
        #for i in range(0, (struct.unpack('>I', self.ihdr_height)[0] * struct.unpack('>I', self.ihdr_width)[0] + 1) * 3, struct.unpack('>I', self.ihdr_width)[0]):
        ##for i in range(1, (struct.unpack('>I', self.ihdr_height)[0] * struct.unpack('>I', self.ihdr_width)[0] + 1) * 3, struct.unpack('>I', self.ihdr_width)[0]):
        #  #for j in range((struct.unpack('>I', self.ihdr_width)[0] * 3) + 1):
        #  #for j in range((struct.unpack('>I', self.ihdr_width)[0] * 3) + 1):
        #  #self.rgb.append(self.data[i:i + 3])

        #  if i % ((struct.unpack('>I', self.ihdr_width)[0] * 3) + 1) == 0:  # filtr -> ten nas nezajima
        #    print("----------------------------------")
        #    print("zacatek radky")
        #    print(self.data[i])
        #    print("----------------------------------")
        #    continue


        #  print(self.data[i])
        #  #self.rgb.append(struct.unpack('>BBB', self.data[i:i + 3]))
        #  #print(self.data[i])

        #for i in range((struct.unpack('>I', self.ihdr_height)[0] * struct.unpack('>I', self.ihdr_width)[0] + 1) * 3):
        # tento cyklus funguje -> prochazeni jednotlivych prvku


        #for i in range(0, (struct.unpack('>I', self.ihdr_height)[0] * struct.unpack('>I', self.ihdr_width)[0] + 1) * 3, (struct.unpack('>I', self.ihdr_width)[0] * 3) + 1):
        for i in range(1, (struct.unpack('>I', self.ihdr_height)[0] * struct.unpack('>I', self.ihdr_width)[0] + 1) * 3, (struct.unpack('>I', self.ihdr_width)[0] * 3) + 1):
          #if i % ((struct.unpack('>I', self.ihdr_width)[0] * 3) + 1) == 0:  # filtr -> ten nas nezajima
          #  continue
          for j in range(0, 3 * struct.unpack('>I', self.ihdr_width)[0], 3):
            print(self.data[i + j: i + j + 3])


          #print(self.data[i])
        #for i in range(struct.unpack('>I', self.ihdr_height)[0]):
        #  for j in range((struct.unpack('>I', self.ihdr_width)[0] * 3) + 1):
        #    for k in range(0, 3):


#            if j == 0:  # zacatek radku -> filtr
#              continue
#
#            print(self.data[3 * i + j])


        print("------------------------------------------------------")

        print(struct.unpack('>I', self.ihdr_width)[0])
        print(struct.unpack('>I', self.ihdr_height)[0])
        print(struct.unpack('>B', self.ihdr_depth)[0])
        print(self.rgb)


        #for i in self.data:
        #  self.data_int.append(int(i, 16))      # konverze na cisla



        ##for i, j in enumerate(self.data):
        ##  if i % 10 == 0:
        ##    self.rgb += self.data[i + 1:]
        ##  print(int(j, 16), i)
        ##  #print(i)

        #for i in range(0, len(self.data_int), 10):
        #  tmp = []
        #  for j in range(1, 10, 3):
        #    #tmp.append(list(self.data_int[i + j:i + j + 3]))
        #    tmp.append(tuple(self.data_int[i + j:i + j + 3]))

        #  #self.rgb.append(self.data_int[i + 1:i + 10])
        #  self.rgb.append(tmp)

        #print(self.rgb)



        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        #self.rgb = []


      # cteni udelat v bloku with -> cteme dany pocet bytu

      # RGB-data obrázku jako seznam seznamů řádek,
      #   v každé řádce co pixel, to trojce (R, G, B)
#      self.rgb = []

