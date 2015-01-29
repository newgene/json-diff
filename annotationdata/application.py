#!/usr/bin/env python
# coding=utf-8

from anno import *

def main():
    url = "http://bioconductor.org/packages/3.0/data/annotation/"
    scratch = ScratchData(3, url, "log.txt")
    tmp = scratch.scratchTable()
    print tmp

if __name__ == "__main__":
    main()
