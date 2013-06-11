#!/usr/bin/python

# walk a directory tree, finding all images *.jpg - "identify" each image

import sys
import os
import getopt
import re
import subprocess

class Chdir(object):
    """
    class to maintain a directory stack
    """
    def __init__(self,directory):
	self.destination = directory

    def __enter__(self):
        if (not self.destination):
            print "Fatal: null destination"
            sys.exit(0)
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
    print "identify all images (*.jpg) in a tree, getting image info"
    print "convert.py [-h --help] [-d --debug] [-r --root (images)] [-v --verbose]]"


def dirGraph(dirname, indent):
    if (verbose):
        print indent+dirname
    fullpath = os.getcwd()
    if os.path.isdir(fullpath):
        for filename in os.listdir(fullpath):
            (name,ext)=os.path.splitext(filename)
            if (ext == ".JPG"):
                print "JPG",filename
                continue
            if (ext != ".jpg"):
                continue
            newname = fullpath + "/" + filename
            if os.path.isdir(newname):
                os.chdir(newname)
                dirGraph(filename,indent+"   ")
            else:
                if (verbose):
                    print indent + "   " + filename
                    
                contentfile = fullpath+'/'+filename

#                cmd='/usr/local/bin/identify "'+contentfile+'"'
                cmd='/usr/local/bin/identify -format "%[fx:w] %[fx:h]" "'+contentfile+'"'

                if (verbose):
                    print cmd
                bufsize=1024
                output = subprocess.Popen(cmd, shell=True, bufsize=bufsize, stdout=subprocess.PIPE).communicate()[0]
                output=output.strip()
                print output,"\t",dirname+"/"+filename


def main(argv):							
    global verbose
    try:
	opts, args = getopt.getopt(argv, "hr:v", ["help","root=","verbose"])
    except getopt.GetoptError:
	usage()
	sys.exit(2)

    root = "images"
    verbose = False
    for opt, arg in opts:
	if opt in ("-h", "--help"):
            usage()
            sys.exit()					
	elif opt in ("-r", "--root"):
            root = arg				 
            print "root",root
	elif opt in ("-v", "--verbose"):
            verbose = True

    with Chdir(root):
        print "walking from root:",root,"\n"
        dirGraph(root,"   ")


if __name__ == "__main__":
	main(sys.argv[1:])
