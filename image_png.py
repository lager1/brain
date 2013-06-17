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

      with open(filepath, 'rb') as f:
        self.header = f.read(8)
        #self.data = f.read()

        if self.header != b'\x89PNG\r\n\x1a\n':
          raise PNGWrongHeaderError("Hlavička zadaného souboru neodpovídá formátu PNG.")


        self.ihdr = f.read(25)  # celkem 25 bytu IHDR chunku
        #self.ihdr = f.read(100)  # celkem 25 bytu IHDR chunku

        print(self.ihdr)




        self.chunk_len = f.read(4)
        #while chunk_len != b'\x00\x00\x00\x00':
        self.chunk_type = f.read(4)    # typ chunku
        self.chunk_len_int = 0

        print(self.chunk_len)
        #print(int(chunk_len, 16))
        #print(int(struct.unpack('>cccc', chunk_len), 16))
        for i, j in enumerate(struct.unpack('>cccc', self.chunk_len)):
          #print(i)
          #print(j)
          #print(int(str(j).strip('b\'').strip('\'')))
          #print(str(j).strip('b\'\\x').strip('\''))
          #print("delka: ")
          #print(int(str(j).strip('b\'\\x').strip('\''), 16))
          #print(255**(4 - i))
          #print(int(str(j).strip('b\'\\x').strip('\''), 16) * 255**(3 - i))
          self.chunk_len_int += int(str(j).strip('b\'\\x').strip('\''), 16) * 255**(3 - i)



          #print(int(j.decode(), 16))
          #print(eval(j))
          #print(j.decode("ascii"))

        #print(struct.unpack(chunk_len)
        print(self.chunk_len_int)
        print(self.chunk_type)



        self.chunk_data = f.read(self.chunk_len_int)
        self.chunk_crc = f.read(4)

        print(self.chunk_data)
        print(self.chunk_crc)

          #chunk_data = 





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

