# -*- coding: utf-8 -*-

import os
import sys
import re
import string
import getopt
import codecs
import traceback
import ntpath

def usage():
    print ("merge_filtered_corpus.py [-i path] [-e extension]")

def load_corpus(input_path, extension):
    try:
        out_path = input_path + "\\merged_corpus.txt"
        out_f = codecs.open(out_path, 'wb', 'utf-8')
        if not os.path.isdir(input_path):
            print ("pass :", input_path)
        else:
            load_corpus_dir(input_path, out_f, extension)
        out_f.close()
    except:
        traceback.print_exc(file=sys.stdout)               
    
def load_corpus_dir(path, out_f, extension):
    flist = os.listdir(path)
    for f in flist:
        next = os.path.join(path, f)
        if os.path.isdir(next):
            load_corpus_dir(next, out_f, extension)
        else:
            if ntpath.basename(path) == "raw" and ntpath.splitext(next)[1] == ("." + extension):
                load_corpus_file(next, out_f)

def load_corpus_file(path, out_f):
    print ("corpus file :", path)
    try:
        in_f = codecs.open(path, 'rb', 'utf-8')
        merge_corpus(in_f, out_f)
        in_f.close()
    except:
        traceback.print_exc(file=sys.stdout)           

def merge_corpus(in_f, out_f):
    count = 0
    while 1:
        line = in_f.readline()
        if not line:
            break
        out_f.write(line)
        count += 1
        if count % 500000 == 0:
            print(".")
            sys.stdout.flush()
            count = 0
        elif count % 10000 == 0:
            print (".", end=" ")
            sys.stdout.flush()
    print ("")
        
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:e:')
        for op, p in opts:
            if op == '-i':
                print ('input path :', p)
                input_path = p
            elif op == '-e':
                print ('extension :', p)
                extension = p                
            else:
                usage()
                sys.exit(2)

        load_corpus(input_path, extension)        
    except:
        usage()
        sys.exit(2)
    
if __name__ == "__main__":
    main(sys.argv[1:])
    