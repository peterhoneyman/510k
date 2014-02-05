####################
# Converts a pdf file into a text file.
# If it runs into some problems, it will flag the file for manual analysis.
# Relies on the Tesseract OCR project and the tesseract-eng library 
#
# Tingyi Wei SPQR Lab, University of Michigan, August 2013: Original code
# Denis Foo Kune, University of Michigan, Feb 2014: Cleanup
####################

# TODO:
# 1. If the folder "txtfile" doesn't exist, create it.
# 2. If the folder "dotfile" doesn't exist, create it.

import sys
import re
from sets import Set
import os

# Global regular expression
rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
minPDF2TEXToutputlength = 50

# Tries pdf2text
# If that doesn't work, does a full blown OCR
def do_ocr(inputfile, outputfile):

  # Checks if the PDF already contains the appropriate text.
  if os.path.exists(inputfile):
    os.system("pdftotext -raw " + inputfile + " " + outputfile)
  else:
    print("Could not open file: " + inputfile)
    return 1


  # process OCR if needed
  # overwrites the old outputfile that contains little output from pdf2txt
  if os.path.getsize("temporary_output.txt") < minPDF2TEXToutputlength:
    print "Doing a full OCR of file: " + inputfile
    data = file(inputfile, "rb").read()
    page_num = len(rxcountpages.findall(data))
    os.system ("#!/bin/sh\nSTARTPAGE=1\nENDPAGE=%s\n" % (page_num) + 
    "SOURCE=" + inputfile + "\nOUTPUT=" + outputfile + "\ntouch $OUTPUT\n" +
    "for i in `seq $STARTPAGE $ENDPAGE`; do\n" + 
    "  convert -monochrome -density 600 $SOURCE\[$(($i - 1 ))\] page.tif\n" +
    "  echo processing page $i\n" +
    "  tesseract page.tif tempoutput -l eng -psm 6\n" +
    "  cat tempoutput.txt >> $OUTPUT\n" +
    "done")

  return 0



# Finds the predicates
# Outputs the edges to stdout
def find_predicate(outputocr, myKnumber):
  #read the whole file for Knumbers
  #Knumbers ("K" followed by 6 digits, ignoring parentheses, dots and whitespace)
  #will be written into predFILE
  #suspicious Knumbers (the six characters following a "K" contain more than 3 digits)
  #will be written into susFILE

  print "Searching for K numbers in file: ", outputocr
  sumfile = open(outputocr)

  Knumbers = Set()

  # Skip over the preamble text to the reply by FDA
  # The reply starts with "Re:" or "re:" and contains the K-number for the device under consideration.
  for line in sumfile:
    if line[0:4] != "Re: ":
      #printline = 0
      indepthInspectionFlag = 0
      manualInspectionFlag = 0

      # Looks for the K number of this device first on the line from the FDA reply
      for idx, char in enumerate(line):
        matchO = re.match(r"(?:(?:\([Kk]\))|[Kk])(?:[\.\s]*\S){6}", line[idx:])

        # We found something.
        # Check if it's a K number by counting the numerical digits.  There should be 6 of them.
        if matchO != None:
          rawKstring = matchO.string[matchO.start():matchO.end()]
          num_digits = len(re.findall(r"\d", rawKstring))

          # We didn't get 6 digits
          # Pocess anyway, but flag for in-depth inspection by the program.
          if num_digits >= 3 and num_digits <= 5:
            #printlinetemp = 1
            indepthInspectionFlag = 1

            # First attempt to grab the K number
            if num_digits == 5 and (rawKstring[0] == 'K' or rawKstring[0] == 'k'):
              # Check for opening brackets and possible mis-ocr 
              # ([dfk] I think this is what's happening)
              if (rawKstring[1] == 'I' or rawKstring[1] == 'i' or rawKstring[1] == '(') and matchO.string[matchO.end()].isdigit():
                rawKstring = rawKstring.replace("(", "")
                rawKstring = rawKstring.replace(")", "")
                rawKstring = rawKstring.replace(".", "")
                rawKstring = rawKstring.replace("i", "")
                rawKstring = rawKstring.replace("I", "")
                rawKstring = "".join(rawKstring.split()) + matchO.string[matchO.end()]

                # Check that the K number that we found is not our own.
                if rawKstring.upper() != myKnumber:
                  # We found a good predicate
                  # accumulate in the current set of K numbers
                  Knumbers.add(rawKstring.upper())  
                # We were able to resolve the issue automatically, 
                # remove the manual check flag.
                indepthInspectionFlag = 0

            # Second atttempt to grab the K number
            # The K string is pretty mangled.
            if indepthInspectionFlag == 1:
              notsusp = rawKstring.find(r"[Kk]", 1)
              while not notsusp == -1:
                if re.match(r"(?:\s*\d){6}", line[notsusp + idx :]) != None:
                  printlinetemp = 0
                notsusp = rawKstring.find(r"[Kk]", notsusp+1)
  
            # The program has not been able to resolve the issues by itself
            # Flags for manual inspection
            if indepthInspectionFlag == 1:
              manualInspectionFlag = 1

          # We got 6 digits, which is the expected outcome
          # We only need to clean up the string
          elif num_digits == 6:
            rawKstring = rawKstring.replace("(", "")
            rawKstring = rawKstring.replace(")", "")
            rawKstring = rawKstring.replace(".", "")
            rawKstring = "".join(rawKstring.split())
            if rawKstring.upper() != myKnumber:
              if sum(rawKstring[i] != myKnumber[i] for i in range(1, 6)) != 1:
                # We found a good K number
                # Accumulate in the set of k numbers.
                Knumbers.add(rawKstring.upper())
              else:
                # Something is not right
                # Flag for human eyes
                manualInspectionFlag = 1

          # TODO: Corner case where we have more than 6 digits
          # one of them is probably a misinterpreted character.  Flag for manual inspection.

      if manualInspectionFlag == 1:
        #SUSfile.write(line)
        print "TODO: ", line 

  if(len(Knumbers) == 0):
    print "Predicates not found"
  else:
    print "Predicates of ", myKnumber, ":"
    for predicate in Knumbers:
      print predicate

  sumfile.close()
  return 0


def main(argv=None):
  
  # Checks if there are enough arguments for an input file
  if len(sys.argv) <= 1:
    print "This program needs at least 1 argument. ", (len(sys.argv) - 1), " arguments given."
    print "Usage: " + sys.argv[0] + " <file.pdf> [output_file.txt]"
    exit(0)
  
  # Rudimentary command line argument processor
  inputocr = sys.argv[1]
  if len(sys.argv) >= 3:
    outputocr = sys.argv[2]
  else:
    outputocr = inputocr + ".ocr.txt"
  # if len(sys.argv) >= 4:
  #   outputedges = sys.argv[3]
  # else
  #   outputocr = inputfile + ".edge.txt"


  # grabs the K number from the filename
  if ((inputocr[0] != 'K') | (len(re.findall(r"\d", inputocr)) < 6)):
    print inputocr,  " does not contain a valid  K number."
    print "The filename must be the FDA K number of the device under consideration."
    print "For example \"K123456.pdf\" contains the summary for device K123456"
    exit(0)
  else:
    myKstring = inputocr[0:7]

  print "processing: ", myKstring, " from file ", inputocr, "->", outputocr

  # Calls the functions that handle the process for OCR and extraction of K numbers
  reterr = do_ocr(inputocr, outputocr)
  if reterr != 0:
    exit(0)     # Something went wrong, bail immediately

    
  reterr = find_predicate(outputocr, myKstring) 
  if reterr != 0:
   exit(0)

  # TODO: cleanup if any


if __name__ == "__main__":
    sys.exit(main())
