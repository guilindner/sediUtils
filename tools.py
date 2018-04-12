
# coding: utf-8

# # Correct Particules after settling
# After the settling simulation, the unwanted particles (above a certain z distance) must be removed from the domain. The objective is to have a flat surface, similar with a channel flow behavior but with a layer of particles on the path. 
# Also, the bottom particles must be frozen, to reduce the computational resources consumed by the simulation.

# Open the file "positions" generated by OpenFOAM for the lagrangian particles
# 
# Open the file "initial_python.in" that was generated for the initial cloud particules used by lammpsFoam

import numpy as np

def loadFile(inputFile):
    with open(inputFile,'r') as f:
        read_data = f.readlines()
    return read_data

def changeAtomType(inputFile,atomType,box):
    read_data = loadFile(inputFile)
    box = np.asarray(box).astype(np.float)
    temp = []
    with open('In_pythonNew.in', 'w') as myfile:
        for i in range(0,10):
            myfile.write(read_data[i])
        myfile.write("\n")
        for i in range(11,len(read_data)):
            temp = read_data[i].split()
            temp = np.asarray(temp).astype(np.float)
            print(box)
            print(temp[4:])
            if (temp[4] > box[0]) and (temp[4] < box[1]) and (temp[5] > box[2]) and (temp[5] < box[3]) and (temp[6] > box[4]) and (temp[6] < box[5]):
                myfile.write(str(int(temp[0]))+" "+str(int(atomType))+" "+str(int(temp[2]))+" "+str(int(temp[3]))+
                             " "+str(temp[4]) +" "+str(temp[5])+" "+str(temp[6])+" "+"\n")
            else:
                myfile.write(str(int(temp[0]))+" "+str(int(temp[1]))+" "+str(int(temp[2]))+" "+str(int(temp[3]))+
                             " "+str(temp[4]) +" "+str(temp[5])+" "+str(temp[6])+" "+"\n")

def keepAtoms(inputFile,box):
    read_data = loadFile(inputFile)
    temp = []
    with open('In_pythonNewKeep.in', 'w') as myfile:
        for i in range(0,10):
            myfile.write(read_data[i])
        myfile.write("\n")
        for i in range(11,len(read_data)):
            temp = read_data[i].split()
            temp = np.asarray(temp)
            if (temp[4] > box[0]) and (temp[4] < box[1]) and (temp[5] > box[2]) and (temp[5] < box[3]) and (temp[6] > box[4]) and (temp[6] < box[5]):
                myfile.write(str(temp[0])+" "+str(temp[1])+" "+str(temp[2])+" "+str(temp[3])+
                             " "+str(temp[4]) +" "+str(temp[5])+" "+str(temp[6])+" "+"\n")
                             
def sumField(inputFile,sumField,th):
    read_data1 = loadFile(inputFile)
    read_data2 = loadFile(sumField)
    cells = int(read_data1[20])
    finalLine = len(read_data1)
    outfile = open('newUb','w')
    count = 0

    for i in range(0,22):
        outfile.write(str(read_data1[i])) 
    for i in range(22,finalLine):
        if read_data2[i] == ')\n':
            line = i
            outfile.write(')\n')
            break
        vortexField = read_data2[i].replace('(','').replace(')','').split()
        initialField = read_data1[i].replace('(','').replace(')','').split()
        arrayVortex = np.asarray(vortexField)
        arrayInitial = np.asarray(initialField)
        arrayVortex = arrayVortex.astype(np.float)
        arrayInitial = arrayInitial.astype(np.float)
        print(arrayVortex[0],arrayVortex[1],arrayVortex[2], th)
        if (abs(arrayVortex[0]) < th) and (abs(arrayVortex[1]) < th) and (abs(arrayVortex[2]) < th):
            count += 1
            result = arrayInitial
        else:
            result = arrayInitial + arrayVortex
        outfile.write('('+str(result[0])+' '+str(result[1])+' '+str(result[2])+')\n')
    for i in range(line+1,finalLine):
        outfile.write(str(read_data1[i]))

    outfile.close()
    print(cells-count,'cells changed from',cells)	                             
