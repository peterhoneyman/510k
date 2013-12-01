# Loads a text file from a directo pdftotxt conversion
# Finds 
#   - The K number of predicates
#   - The regulatory name
#   - Regulatory Class (I, II or III)
#   - Dated
#   - Date received
#
# Basically everythin at the top of the summary from FDA.  It start with "Re:" and the K number for the case.
#
# Outputs a text file with all the vital information about the device
# Format:
# knumber, name, regNumber, regName, regClass, productCode, dateSubmitted, dateReceived
#
# Denis Foo Kune, University of Michigan, 2013


import sys
import re

# Given the raw text data from the pdftotext program, find the section from the FDA
# Returns a list of 7 parts
def getSummary(filename):
    f = open(filename, "r")
    infolist = list()
    highlight = 0
    for line in f:
        # Get the next line that has text
        if (highlight > 0) & (len(line)>5):
            # Clean the line
            cleanline = line.strip()
            infolist.append(cleanline)
            if highlight > 7:
                # We are done
                return infolist

        # Finds the string "Re:"
        # Starts the line search
        print line
        if re.search("Re:", line) != None:
            print "Found"
            # TODO: Find K number in that string (to double check)
            
            # Returns the next 7 lines that contain text
            highlight =  1


def getDeviceName(strlist):
    retstr = ""
    for line in strlist:
        # Find the line containing "Trade" and "Device" and "Name"
        if re.search("Trade", line) != None:
            subtext = line.split(":")
            retstr = subtext[1].strip()
            return retstr
    return None

def getRegulationNumber(strlist):
    retstr = ""
    for line in strlist:
        # Find the line containing "Trade" and "Device" and "Name"
        if re.search("Regulation Number", line) != None:
            subtext = line.split("Regulation Number")
            tmpstr = subtext[1].strip()
            # Remove the leading ":" or possible mis-OCR'd version of it
            retstr = tmpstr[2:len(tmpstr)]
            return retstr
    return None


def getRegulationName(strlist):
    retstr = ""
    return retstr


def getRegulationClass(strlist):
    retstr = ""
    return retstr

def getProductCode(strlist):
    retstr = ""
    return retstr

def getDateSubmitted(strlist):
    retstr = ""
    return retstr

def getDateReceived(strlist):
    retstr = ""
    return retstr


# Call this with the appropriate key values
# The list of key string that should appear are listed as follows.
#
# Trade/Device Name
# Regulation Number
# Regulation Name
# Regulatory Class
# Product Code
# Dated
# Received

def getStringValue(strlist, itemkey):
    retstr = ""
    for line in strlist:
        # Find the line containing "Trade" and "Device" and "Name"
        if re.search(itemkey, line) != None:
            subtext = line.split(itemkey)
            tmpstr = subtext[1].strip()
            # Remove the leading ":" or possible mis-OCR'd version of it
            retstr = tmpstr[2:len(tmpstr)]
            return retstr
    return None



def loadfile(name):
    f = open(name, "r")
    


def main(argv=None):
    #------------------------
    # Argument processing.
    #------------------------
    # if argv is None:
    #     argv = sys.argv
    # try:
    #     try:
    #         opts, args = getopt.getopt(argv[1:], "h", ["help"])
    #     except getopt.error, msg:
    #          raise Usage(msg)
    #     # more code, unchanged
    # except Usage, err:
    #     print >>sys.stderr, err.msg
    #     print >>sys.stderr, "for help use --help"
    #     return 2

    print "Hello 510(k)"
    summary = getSummary("K022597.txt")
    print summary


if __name__ == "__main__":
    sys.exit(main())
