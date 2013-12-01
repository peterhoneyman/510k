import sys
from PIL import Image

# The dictionaries that holds all the device relations.
predicates = dict()
parents = dict()

# Maps k numbers to unique sequential integers
# Note: The sequence numbers can change if the devices are sorted by K-numbers, class or type.
kmap = dict()
karray = dict()

# Output image parameters
binsize = 100


# Takes the karray bitmap and draws the pixels, grouping them in chunks of 100
def renderImage():
    img = Image.new("RGB", (1 + len(karray)/binsize, 1 + len(karray)/binsize))
    pix_y = 0
    bin_y = 0
    #print "karray[item]:", len(karray)
    for row in karray:
        bin_x = 0
        pix_x = 0
        pixcolor = 255
        bin_y += 1
        for item in karray[row]:
            bin_x += 1
            if item > 0:
                pixcolor -= 50
            # When the vin is full, we set the appropriate color and move to the next bin
            if bin_x >= binsize:
                img.putpixel((pix_x,pix_y),(pixcolor, pixcolor, pixcolor))
                bin_x = 0
                pix_x += 1
                pixcolor = 255
        if bin_y >= binsize:
            print "pix_y: ", pix_y, "(",len(karray)/binsize,")"
            bin_y = 0
            pix_y += 1

    img.save("test.png")

    


# Assumes that the dictionary is sorted the way we want it.
# TODO:  Sort entries here.
def buildmapUsing(thisdict):
    counter = 0
    for item in thisdict:
        # The kmap will allow us to walk down the columns
        kmap[item] = counter
        counter += 1

    # Populates the array.
    arraylen = len(thisdict)
    for item in thisdict:
        # Makes arrays for each row
        newrow = bytearray(arraylen)
        # Populate the row
        ks = thisdict[item]
        for device in ks:
            try:
                newrow[kmap[device]] = 1  
            except KeyError:
                # Skip this entry
                #print "Device not found: ", device
                c = 1
        karray[item] = newrow
        # print "Arraylen:", arraylen, " newrow:", len(newrow), " karray[item]:", len(karray[item])


def populateDict(mydict, device, related):
    if device in mydict:
        # add related to the set
        mydict[device].add(related)
    else: 
        # New entry
        a = set()
        a.add(related)
        mydict[device] = a


def loadFile(filename=None):
    if filename == None:
        return
    f = open(filename, "r")
    for line in f:
        # split string into device and predicate
        # then populate dictionary
        tokens = line.strip().partition(" ")
        a = tokens[0]
        b = tokens[2]
        # populate table with egress links
        populateDict(predicates, a, b)
        # populate table with ingress links
        populateDict(parents, b, a)



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
    loadFile("large.txt")
    print "Loaded Large.txt file done.  Predicate:", len(predicates), " Parents:", len(parents)

    # All the devices are loaded.  Populate a matrix of all devices
    # builds a map between Knumbers and sequential access numbers
    if len(predicates) > len(parents):
        buildmapUsing(predicates)
    else:
        buildmapUsing(parents)

    #print karray
    # Build a matrix illustrating the relationships
    renderImage()

if __name__ == "__main__":
    sys.exit(main())
