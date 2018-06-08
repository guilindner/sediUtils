#!/usr/bin/env/ python3

#Atoms/particle definition
atoms = {'nType' : 2, 'diameter' : 0.0005, 'std_diameter' : 0.0000,'density' : 2500}

# Domain definition, where the simulation happens
domainBox = [0.0, 0.1, 0.0, 0.1, 0.0, 0.05]

#Conserved domain, particles out of this box will be removed
safeBox = [0.0, 0.1, 0.0, 0.1, 0.0, 0.01]

#Active domain, particles out of this box will be frozen
activeBox = [0.04, 0.09, 0.00, 0.1, 0.005, 0.05]
