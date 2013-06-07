#!/opt/python3.3/bin/python3.3
# encoding: utf-8

class PNGWrongHeaderError(Exception):
    """Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""

    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)

class PNGNotImplementedError(Exception):
    """Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""
    pass


class PngReader():
    """Třída pro práci s PNG-obrázky."""

    def __init__(self, filepath):

      with open(filepath, 'rb') as f: 
        header = f.read(8)
#        header = struct.unpack("=cccccccc", header)
      if header != b'\x89PNG\r\n\x1a\n':
        raise PNGWrongHeaderError("Hlavička zadaného souboru neodpovídá formátu PNG.")

      else:
        print("je png")


      # RGB-data obrázku jako seznam seznamů řádek,
      #   v každé řádce co pixel, to trojce (R, G, B)
#      self.rgb = []

