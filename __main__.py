#!/opt/python3.3/bin/python3.3
# encoding: utf-8


# ------------------------------------------------------------------------------
#    semestralni prace z predmetu BI-PYT, FIT CVUT, letni semestr 2013
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
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

  if args.file != "":
    if args.braincopter == True:
      brainx.BrainCopter(args.file)

    elif args.brainloller == True:
      brainx.BrainLoller(args.file)

    else:
      brainx.BrainFuck(args.file)

  else:
    print("nebyl zadan zadny soubor")
    exit(1)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
  main()


