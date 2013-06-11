#!/usr/bin/python

# walk a directory tree, finding all images *.jpg

import sys
import os
import getopt
import re
import subprocess


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
    print "convert all images in a tree, creating converted"
    print "convert.py [-h --help] [-d --debug] [-r --root (images)] [-v --verbose] [-t --converted (converted)]"


def dirGraph(dirname, converted, indent):
    if (verbose):
        print indent+dirname
    fullpath = os.getcwd()
    if os.path.isdir(fullpath):
        for filename in os.listdir(fullpath):
            (name,ext)=os.path.splitext(filename)
            if (ext == ".JPG"):
                print "JPG",filename,"************************"
                continue
            if (ext != ".jpg"):
                continue

            newname = fullpath + "/" + filename
            if os.path.isdir(newname):
                os.chdir(newname)
                dirGraph(filename,converted,indent+"   ")
            else:
                if (verbose):
                    print indent + "   " + filename
                    
                contentfile = fullpath+'/'+filename
                convertednailfilename = converted+'/'+filename

                cmd='/usr/local/bin/convert -sample 2000 "'+contentfile+'" "'+convertednailfilename+'"'

                print cmd

                bufsize=1024
                output = subprocess.Popen(cmd, shell=True, bufsize=bufsize, stdout=subprocess.PIPE).communicate()[0]
                print output

def main(argv):							
    global verbose
    try:
	opts, args = getopt.getopt(argv, "dr:vc:", ["root=","converted=","dir","verbose"])
    except getopt.GetoptError:
	usage()
	sys.exit(2)

    root = "art"
    converted="artConverted"
    verbose = False
    for opt, arg in opts:
	if opt in ("-h", "--help"):
            usage()
            sys.exit()					
	if opt in ("-d", "--debug"):
            global _debug				
            _debug = 1					

	elif opt in ("-r", "--root"):
            root = arg				 
	elif opt in ("-c", "--converted"):
            converted = arg				 
	elif opt in ("-v", "--verbose"):
            verbose = True


    if not os.path.isdir(converted):
        print "no dir",converted
        os.mkdir("./"+converted)
    with Chdir(root):
        print "walking from root:",root,"\n"
        dirGraph(root,"../"+converted,"   ")


if __name__ == "__main__":
	main(sys.argv[1:])
