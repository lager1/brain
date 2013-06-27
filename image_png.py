#!/opt/python3.3/bin/python3.3
# encoding: utf-8

# ------------------------------------------------------------------------------
import struct
import zlib

# ------------------------------------------------------------------------------
class PNGWrongHeaderError(Exception):
    """Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""

    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)

# ------------------------------------------------------------------------------
class PNGNotImplementedError(Exception):
    """Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""

    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)


# ------------------------------------------------------------------------------
class PNGWrongCrcError(Exception):
    """Výjimka oznamující, že PNG-obrázek je poškozen."""

    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)


# ------------------------------------------------------------------------------
class PngReader():
    """Třída pro práci s PNG-obrázky."""


# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
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

                        if i < 1 and j < 1:
                            for k in range(3):
                                self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + self.paeth(0, 0, 0)) & 0xff)

                        elif j < 1:
                            for k in range(3):
                                self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + self.paeth(0, self.rgb[i - 1][1][j][k], 0)) & 0xff)

                        elif i < 1:
                            for k in range(3):
                                self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + self.paeth(self.rgb[i][1][j - 1][k], 0, 0)) & 0xff)

                        else:
                            for k in range(3):
                                self.rgb[i][1][j][k] = ((self.rgb[i][1][j][k] + self.paeth(self.rgb[i][1][j - 1][k], self.rgb[i - 1][1][j][k], self.rgb[i - 1][1][j - 1][k])) & 0xff)

                    self.pix.append(self.rgb[i][1])    # pridame do vysledku radek bez filtru

            self.rgb = []
            # konverze na trojice rgb hodnot
            for i in self.pix:
                self.tmp = []
                for j in i:
                    self.tmp.append(tuple(j))
                self.rgb.append(self.tmp)


