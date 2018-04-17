#!/usr/bin/env/ python3
"""vortex detection tool, by Guilherme Lindner, 2017-04\n
This program load NetCDF files from DNS simulations  or PIV experiments
and detect the vortices and apply a fitting to them.
"""
import sys
import argparse
import numpy as np

import tools
import config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', dest='inputFile',
                        default='',
                        help='input file', metavar='FILE')
    parser.add_argument('-s', '--sumField', dest='sumField',
                        default='none',
                        help='input file to be added', metavar='FILE')
    parser.add_argument('-g', action='store_true',
                        help='generate atoms inside the domain')
    parser.add_argument('-c', action='store_true',
                        help='convert from OpenFoam to LAMMPS')
    parser.add_argument('-r', action='store_true',
                        help='remove atoms outside the safeBox')
    parser.add_argument('-f', action='store_true',
                        help='freeze all particles')
    parser.add_argument('-a', action='store_true',
                        help='activate the atoms inside activeBox')


    args = parser.parse_args()
    
    if args.g == True:
        tools.generateAtoms(config.atoms, config.domainBox, config.safeBox)
    if args.c == True:
        tools.ofToLammps(args.inputFile, config.atoms, config.domainBox, config.safeBox) 
    if args.r == True:
        tools.removeAtoms(args.inputFile, config.atoms, config.safeBox)
    if args.f == True:
        tools.removeAtoms(args.inputFile)
    if args.atomType != 0:
        tools.changeAtomType(args.inputFile, args.atomType, args.box)


    if args.sumField != 'none':
       tools.sumField(args.inputFile, args.sumField)
