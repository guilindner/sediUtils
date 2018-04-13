#!/usr/bin/env/ python3
"""vortex detection tool, by Guilherme Lindner, 2017-04\n
This program load NetCDF files from DNS simulations  or PIV experiments
and detect the vortices and apply a fitting to them.
"""
import sys
import argparse
import numpy as np

import tools

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', dest='inputFile',
                        default='',
                        help='input file', metavar='FILE')
    parser.add_argument('-s', '--sumField', dest='sumField',
                        default='none',
                        help='input file to be added', metavar='FILE')
    parser.add_argument('-t', '--threshold', dest='threshold', default=0.001, type=float,
                        help='threshold for the small velocity components')
    parser.add_argument('-a', '--atomType', dest='atomType', default=0, type=int,
                        help='change the atom type')
    parser.add_argument('-k', '--keepAtoms', dest='keepAtoms',default=False, type=bool,
                        help='keep atoms inside the box and remove the others')
    parser.add_argument('-b', '--box', nargs=6, dest='box', default=[0.0,1.0,0.0,1.0,0.0,1.0],
                        help='change the atom type on specific box. ex: -a 2 0.0 0.2 0.0 0.1 0.0 0.9')

    args = parser.parse_args()
    
    if args.atomType != 0:
        tools.changeAtomType(args.inputFile, args.atomType, args.box)
    if args.keepAtoms == True:
        tools.keepAtoms(args.inputFile, args.box)        
    if args.sumField != 'none':
       tools.sumField(args.inputFile, args.sumField)
