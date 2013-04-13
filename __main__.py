#!/opt/python3.3/bin/python3.3
# encoding: utf-8


''' ------------------------------------------------------------------------------

    semestralni prace z predmetu BI-PYT, FIT CVUT, letni semestr 2013

    ------------------------------------------------------------------------------
'''



# ------------------------------------------------------------------------------
# import knihoven
# ------------------------------------------------------------------------------
import os
import sys
import argparse
import brainx


# ------------------------------------------------------------------------------
# definice hlavni funkce
# ------------------------------------------------------------------------------
def main():
  parser = argparse.ArgumentParser(description='Interpretr jazyka brainfuck.')
  parser.add_argument('--version', action='version', version='0.1', help='show program\'s version number and exit')
  parser.add_argument('-l', '--brainloller', action='store_true', help='Jde o program v jazyce brainloller.')
  parser.add_argument('-c', '--braincopter', action='store_true', help='Jde o program v jazyce braincopter.')
  parser.add_argument('file', help='Soubor ke zpracování.')

  args = parser.parse_args()
  print(args)

  if os.path.isfile(args.file):     # soubor
    print("soubor existuje")

  elif args.file == "":
    sys.exit("zadany soubor \"" + args.file + "\" neexistuje")

  else:                             # kod primo na radce
    pass






# ------------------------------------------------------------------------------
if __name__ == "__main__":
  main()


