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
          raise PNGWrongHeaderError("Strukturu zadaného souboru není možné zpracovat.")

        self.ihdr_width = f.read(4)  # vyska obrazku v pixelech
        self.ihdr_height = f.read(4) # sirka obrazku v pixelech
        self.ihdr_depth = f.read(1)  # bitova hloubka
        self.ihdr_col_type = f.read(1)   # barvovy typ
        self.ihdr_compression = f.read(1)   # metoda komprese
        self.ihdr_filter = f.read(1)        # metoda filtrace
        self.ihdr_interlace = f.read(1)     # metoda prokladani
        self.ihdr_crc = f.read(4)     # kontrolni soucet


        #print(self.ihdr_len)
        #print(struct.unpack('>cccc', self.ihdr_len))
        #print("------------------------------------------------------")

        self.chunk_len = f.read(4)
        while chunk_len != b'\x00\x00\x00\x00':     # cteni vseho az do IEND

          self.chunk_type = f.read(4)    # typ chunku

          if self.chunk_type != b'IDAT':
            raise PNGWrongHeaderError("Strukturu zadaného souboru není možné zpracovat.")

          self.chunk_len_int = 0
          self.idat = b''

          #print(self.chunk_len)
          #print(int(chunk_len, 16))
          #print(int(struct.unpack('>cccc', chunk_len), 16))


          # toto chce udelat nejak lepe, nebude to fungovat vzdy
          for i, j in enumerate(struct.unpack('>cccc', self.chunk_len)):
            #print(i)
            #print(j)
            #print(int(str(j).strip('b\'').strip('\'')))
            #print(str(j).strip('b\'\\x').strip('\''))
            #print("delka: ")
            #print(int(str(j).strip('b\'\\x').strip('\''), 16))
            #print(255**(4 - i))
            #print(int(str(j).strip('b\'\\x').strip('\''), 16) * 255**(3 - i))
            self.chunk_len_int += int(str(j).strip('b\'\\x').strip('\''), 16) * 256**(3 - i)



            #print(int(j.decode(), 16))
            #print(eval(j))
            #print(j.decode("ascii"))

          #print(struct.unpack(chunk_len)



          self.chunk_data = f.read(self.chunk_len_int)
          self.idat += self.chunk_data
          self.chunk_crc = f.read(4)


          print(self.chunk_len_int)
          print(self.chunk_type)
          print(self.chunk_data)
          print(self.chunk_crc)

          self.chunk_len = f.read(4)

          #chunk_data = 


        self.iend_len = f.read(4)    # delka
        self.iend_type = f.read(4)   # typ
        self.iend_crc = f.read(4)   # crc

        print("------------------------------------------------------")

        print(self.iend_len)
        print(self.iend_type)
        print(self.iend_crc)

        rest = f.read()

        print(rest)
        print("------------------------------------------------------")
        #print(zlib.decompress(self.chunk_data))
        print(zlib.decompress(self.idat))



        print("------------------------------------------------------")



        self.data = str(zlib.decompress(self.idat)).strip('b\'\\x').strip('\'').split('\\x')
        self.data_int = []

        for i in self.data:
          self.data_int.append(int(i, 16))      # konverze na cisla



        #for i, j in enumerate(self.data):
        #  if i % 10 == 0:
        #    self.rgb += self.data[i + 1:]
        #  print(int(j, 16), i)
        #  #print(i)

        for i in range(0, len(self.data_int), 10):
          tmp = []
          for j in range(1, 10, 3):
            #tmp.append(list(self.data_int[i + j:i + j + 3]))
            tmp.append(tuple(self.data_int[i + j:i + j + 3]))

          #self.rgb.append(self.data_int[i + 1:i + 10])
          self.rgb.append(tmp)

        print(self.rgb)

        #self.rgb = []   # vycisteni, pouze debug


        # kazde 3 byty jsou prefixovany 0


        #print(zlib.decompress(self.idat))


#        for i in range(0, len(zlib.decompress(self.idat)), 3):




        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        #self.rgb = []




        #self.data = f.read()

        #print(self.data[:4])  # hlavicka
        #print(self.data[4:8])  # IHDR
        #print(self.data[8:21])  # data
        #print(self.data[21:25])  # crc

        #print("")
        #print("")
        #print("")
        #print("")
        #print(self.data)

      # cteni udelat v bloku with -> cteme dany pocet bytu

      # RGB-data obrázku jako seznam seznamů řádek,
      #   v každé řádce co pixel, to trojce (R, G, B)
#      self.rgb = []

