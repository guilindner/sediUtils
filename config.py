#!/usr/bin/env/ python3

# Atoms/particle definition
atoms = {'nType' : 2, 'diameter' : 0.0005, 'std_diameter' : 0.0000,'density' : 2500}

# Domain and mesh definition, where the simulation happens
domainBox = [0.0, 0.1, 0.0, 0.1, 0.0, 0.05]
mx=200
my=200
mz=100

# Conserved domain, particles out of this box will be removed
safeBox = [0.0, 0.1, 0.0, 0.1, 0.0, 0.01]

# Active domain, particles out of this box will be frozen
activeBox = [0.00, 0.1, 0.00, 0.1, 0.005, 0.05]

# Flow properties
flow=0.23
k=0.01

# Vortex properties
vortexR=0.006
vortexS=80

# Simulation parameters
settleTime=0.5
flowTime=0.25
convectTime=0.5
