####################
# This program is used to download the
# summary files from the FDA 510(K) database
# @Author: Tingyi Wei SPQR Lab, University of Michigan
# August 2013
####################

# TODO:
# 1. Create the "pdffile" folder if it doesn't exist.


import sys
import re
import urllib2
import os

def find_predicate(SUMfile, device):
  #Download decision file if available
  review_file = 1
  url = "http://www.accessdata.fda.gov/cdrh_docs/reviews/" + device + ".pdf"

  file_name = url.split('/')[-1]
  try:
    u = urllib2.urlopen(url)
  except urllib2.HTTPError, e:
    review_file = 0

  #Download summary file if decision file not available
  if review_file == 0:
    pdfnum = device[1:3]
    if device[1:3] == "00" or device[1:3] == "01" or device[1:2] == "9":
      pdfnum = ""
    elif device[1:2] == "0":
      pdfnum = device[2]
      
    url = "http://www.accessdata.fda.gov/cdrh_docs/pdf" + pdfnum + "/" + device + ".pdf"

    try:
      u = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
      SUMfile.write( device + " File not found\n")
      return
  
  f = open("pdffile/" + file_name, 'wb')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])

  file_size_dl = 0
  block_sz = 8192
  while True:
    buffer = u.read(block_sz)
    if not buffer:
      break
  
    f.write(buffer)
  f.close()
  

  SUMfile.write( "%s review: %s\n" % (device, review_file))


PMNfile = open(sys.argv[1])
SUMfile = open(sys.argv[2], 'w')
next(PMNfile)

for line in PMNfile:
  n = 14
  start = line.find('|')
  while start >= 0 and n > 1:
    start = line.find('|', start + 1)
    n -= 1
  end = line.find('|', start + 1)
  if line[start + 1:end] == "Summary":
    if line[0] != 'K' or not (line[1:7]).isdigit():
      SUMfile.write( "device Knumber error\n")
    else:
      find_predicate(SUMfile, line[0:7])
  elif line[start + 1:end] == "Statement":
    SUMfile.write( line[0:7] + " Summary not available\n")
  else:
    if line[0] != 'K' or not (line[1:7]).isdigit():
      SUMfile.write( "device Knumber error\n")
    else:
      find_predicate(SUMfile, line[0:7])

PMNfile.close()
SUMfile.close()
