#!/usr/bin/env/ python3

#Atoms/particle definition
atoms = {'nType' : 2, 'diameter' : 0.0005, 'density' : 2650}

# Domain definition, where the simulation happens
domainBox = [0.0, 0.1, 0.0, 0.06, 0.0, 0.03]

#Conserved domain, particles out of this box will be removed
safeBox = [0.0, 0.1, 0.0, 0.007, 0.0, 0.03]

#Active domain, particles out of this box will be frozen
activeBox = [0.3, 0.7, 0.0, 0.06, 0.0, 0.03]
