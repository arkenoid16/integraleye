#!/usr/bin/python

# walk a directory tree, finding all images *.jpg
# create an MRSS feed file

import sys
import os
import getopt
import re

urlRoot="http://www.theintegraleye.com/"

class Chdir(object):
    """
    class to maintain a directory stack
    """
    def __init__(self,directory):
	self.destination = directory

    def __enter__(self):
	self.cwd = os.getcwd()
	try:
            os.chdir(self.destination)
	except:
            print "Fatal: cannot find " + self.destination
            sys.exit(0)

    def __exit__(self,eType,eInstruction,eTB):
	if eType:
            print eType,eInstruction
	os.chdir(self.cwd)

def usage():
    print "create an MRSS feed from a directory of images"
    print "walk.py [-h --help] [-d --debug] [-r --root root (images)] [-v --verbose]"

def dirGraph(dirname, indent, outputfile):
    if (verbose):
        print indent+dirname
#    print indent+os.getcwd()
    imageCount=0
    fullpath = os.getcwd()
    if os.path.isdir(fullpath):
        l=open(dirname+".lst","r")
        filelist=l.readlines()
        for filename in filelist:
            imageCount+=1
            filename=filename.strip()
            try:
                d=open(filename+".txt","r")
                line=d.readline()
                line=line.replace('\r',' ')
                line=line.replace('\n',' ')
            except IOError:
                line=""
            if (verbose):
                print
                print line
            filename=filename+".jpg"
            newname = fullpath + "/" + filename
            if os.path.isdir(newname):
                os.chdir(newname)
                dirGraph(filename,indent+"   ",outputfile)
            else:
                linkname = urlRoot+'images/'+dirname+'/'+filename

                contentfile = 'assets/images/'+dirname+'/'+filename
                thumbnailfile = 'assets/images/'+dirname+'/'+filename

                outputfile.write('          <item>\n')
                outputfile.write('               <title>'+filename+'</title>\n')
                outputfile.write('               <description>'+line+'</description>\n')
                outputfile.write('               <link>'+linkname+'</link>\n')  # note link to full resolution file
                outputfile.write('               <guid>'+linkname+'</guid>\n')
                outputfile.write('               <thumbnail>'+thumbnailfile+'</thumbnail>\n')
                outputfile.write('               <content>'+contentfile+'</content>\n')
                outputfile.write('          </item>\n\n')
    print dirname + " imageCount "
    print str(imageCount)

def main(argv):							
    global verbose
    try:
	opts, args = getopt.getopt(argv, "dhr:v", ["debug","help","root=","verbose"])
    except getopt.GetoptError:
        print "options error"
	usage()
	sys.exit(2)

    root = "images"
    verbose = False

    for opt, arg in opts:
	if opt in ("-h", "--help"):
            usage()
            sys.exit()					

	elif opt in ("-d", "--debug"):
            global _debug				
            _debug = 1					

	elif opt in ("-r", "--root"):
            root = arg				 
            print "root ",root

	elif opt in ("-v", "--verbose"):
            verbose = True

    xmlFileName=root+".xml"
    outputfile = open(xmlFileName,"w")
    outputfile.write('<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>\n')
    outputfile.write('<rss version="2.0"\n')
    outputfile.write('\txmlns:media="http://search.yahoo.com/mrss/"\n')
    outputfile.write('\txmlns:atom="http://www.w3.org/2005/Atom">\n')

    outputfile.write('    <channel>\n')
    outputfile.write('          <title>Integraleye First Release</title>\n')
    outputfile.write('          <description>many beautiful pictures in '+root+'</description>\n')
    outputfile.write('          <link>http://www.theintegraleye.com</link>\n')

    outputfile.write('          <atom:link href="http://www.theintegraleye.com/feed.xml" rel="self" type="application/rss+xml" />\n')

    with Chdir(root):
        dirGraph(root,"   ",outputfile)

        outputfile.write('      </channel>\n')
        outputfile.write('</rss>\n')

        outputfile.close()


if __name__ == "__main__":
	main(sys.argv[1:])
