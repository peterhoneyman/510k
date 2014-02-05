This set of programs analyzes the 510(k) dependency graph.  It works in 3 stages.

1. Downloads the summary files of the cleared devices from the U.S. Food and Drug Administration (FDA) 510(k) database.
2. Runs a Optical Character Recognition (OCR) program to 


-----------------
python download.py [510k_pmn_file] [summary]

[510k_pmn_file]: The input file is a pmn file downloaded from the FDA 510(K) database.  The PMN files are lists of devices cleared.  The PMN files from the FDA are available here:
http://www.fda.gov/MedicalDevices/ProductsandMedicalProcedures/DeviceApprovalsandClearances/510kClearances/ucm089428.htm

[summary]: The output is a summary file contain the information of whether the files are available for download for each device mentioned in the PMN list.

This program then downloads the available summary files from the FDA 510(K) database and stores them in a folder called "pdffile".


---------------
python predocr.py [Knumber] [outputOCRname]

[summary]: mandatory pdf file to be processed.  The file name should be the K-number, per FDA common practice.  i.e. K123456.pdf contains the summary for device K123456.

[outputOCR] optional file to hold the output of the OCR process.  If ommited, a filename with the K-number, appended with ".ocr.txt" will be generated.

TODO:  Wrapping script to loop through all pdf files.

*** DEPRECATED ***
python predocr.py [summary] [predfile] [susfile]

[summary]: The input file is the summary file in PDF format obtained from FDA 510k database.

[predfile]: The output predicate file which contains a list of each device and its predicates.

[susfile]: The output suspicious or uncertain file contains lines in the resulting predicate file which may contain some Knumbers that are miss-translated by OCR.  Those lines are candidate for manual inspection.

This program transform the pdf files into ascii text format (in a folder "txtfile"), and then search for and record the Knumbers in each file.


--------------
python plotGraph.py [predfile] [group] [stacfile] [degreefile] [redundant_pathfile]

[predfile]: The input file is the predfile containing the list of devices and their predicates.

[group]: The output group file records the Knumber of devices in each graph.

[stacfile]: The output stac file records the number of nodes in each graph.

[degreefile]: The degree file records the number of edges pointing in and out of each node.

[redundant_pathfile]: The redundant_path file records the number of redundant paths between each device and
its predicates.

This program separates the devices into groups according to the predicate relationship, and generates GraphViz ".dot" files into a folder "dotfile" which could be used to generate the predicate graph with software XDot.


--------------
End
