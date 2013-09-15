####################
# This program is used to transform the 
# summaries files downloaded from the FDA
# 510(k) databse to readable txt format, 
# and find the predicates Knumbers.
# @Author: Tingyi Wei SPQR Lab, University of Michigan
# August 2013
####################

# TODO:
# 1. If the folder "txtfile" doesn't exist, create it.
# 2. If the folder "dotfile" doesn't exist, create it.

import sys
import re
from sets import Set
import os

rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)

#function to find the predicates Knumber given the scanned pdf file
def find_predicate(device, TREEfile, SUSfile):
  #use pdftotext to get readable txt files
  if os.path.exists("pdffile/" + device + '.pdf'):
    os.system("pdftotext -raw " + "pdffile/" + device + ".pdf txtfile/" + device + ".txt")
  else:
    TREEfile.write(device + ": " + "file not downloaded\n")
    return

  if not os.path.exists("txtfile/" + device + '.txt'):
    TREEfile.write(device + ": " + "pdf to text error\n")
    return

  #process OCR if needed
  if os.path.getsize("txtfile/" + device + '.txt') < 50:
    print device
    data = file("pdffile/" + device + '.pdf', "rb").read()
    page_num = len(rxcountpages.findall(data))
    os.system ("#!/bin/sh\nSTARTPAGE=1\nENDPAGE=%s\n" % (page_num) + 
    "SOURCE=pdffile/" + device + ".pdf\nOUTPUT=txtfile/" + device + ".txt\ntouch $OUTPUT\n" +
    "for i in `seq $STARTPAGE $ENDPAGE`; do\n" + 
    "  convert -monochrome -density 600 $SOURCE\[$(($i - 1 ))\] page.tif\n" +
    "  echo processing page $i\n" +
    "  tesseract page.tif tempoutput -l eng -psm 6\n" +
    "  cat tempoutput.txt >> $OUTPUT\n" +
    "done")

  #read the whole file for Knumbers
  #Knumbers ("K" followed by 6 digits, ignoring parentheses, dots and whitespace)
  #will be written into predFILE
  #suspicious Knumbers (the six characters following a "K" contain more than 3 digits)
  #will be written into susFILE
  sumfile = open("txtfile/" + device + '.txt')

  Knumbers = Set()
  SUSfile.write('*' + device + '*\n')
  for line in sumfile:
    if line[0:4] != "Re: ":
      printline = 0

      for idx, char in enumerate(line):
        matchO = re.match(r"(?:(?:\([Kk]\))|[Kk])(?:[\.\s]*\S){6}", line[idx:])

        if matchO != None:
          exp = matchO.string[matchO.start():matchO.end()]
          num_digits = len(re.findall(r"\d", exp))
          if num_digits >= 3 and num_digits <= 5:
            printlinetemp = 1
            if num_digits == 5 and (exp[0] == 'K' or exp[0] == 'k'):
              if (exp[1] == 'I' or exp[1] == 'i' or exp[1] == '(') and matchO.string[matchO.end()].isdigit():
                exp = exp.replace("(", "")
                exp = exp.replace(")", "")
                exp = exp.replace(".", "")
                exp = exp.replace("i", "")
                exp = exp.replace("I", "")
                exp = "".join(exp.split()) + matchO.string[matchO.end()]
                if exp.upper() != device:
                  Knumbers.add(exp.upper())  
                printlinetemp = 0
            if printlinetemp == 1:
              notsusp = exp.find(r"[Kk]", 1)
              while not notsusp == -1:
                if re.match(r"(?:\s*\d){6}", line[notsusp + idx :]) != None:
                  printlinetemp = 0
                notsusp = exp.find(r"[Kk]", notsusp+1)
  
            if printlinetemp == 1:
              printline = 1
      
          elif num_digits == 6:
            exp = exp.replace("(", "")
            exp = exp.replace(")", "")
            exp = exp.replace(".", "")
            exp = "".join(exp.split())
            if exp.upper() != device:
              if sum(exp[i] != device[i] for i in range(1, 6)) != 1:
                Knumbers.add(exp.upper())
              else:
                printline = 1    

      if printline == 1:
        SUSfile.write(line)

  TREEfile.write(device + ': ')
  if(len(Knumbers) == 0):
    TREEfile.write("Predicates not found")
  else:
    for Knumber in Knumbers:
      TREEfile.write(Knumber + " ")
  TREEfile.write('\n')

  sumfile.close()


SUMfile = open(sys.argv[1])
TREEfile = open(sys.argv[2], 'w')
SUSfile = open(sys.argv[3], 'w')

for line in SUMfile:
  if line[8] == 'r':
    find_predicate(line[0:7], TREEfile, SUSfile)
  elif line[8] == 'F':
    TREEfile.write(line[0:7] + ": File not found\n")
  elif line[9] == 'u':
    TREEfile.write(line[0:7] + ": Summary not available\n")
  elif line[9] == 't':
    TREEfile.write(line[0:7] + ": Statment and summary error!\n")

SUMfile.close()
TREEfile.close()
SUSfile.close()
