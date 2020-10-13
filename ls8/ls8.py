#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def main(argv):
    if len(argv) != 2:
        print(f"Usage: {argv[0]} filname", file=sys.stderr)     
        return 1
    
    cpu = CPU()

    cpu.load(argv[1]) #take the program which is 8 
    cpu.run() #then runs the prorgram by print 8 
    return 0 


if __name__ == "__main__":
    sys.exit(main(sys.argv))