import numpy as np

def loadFile(inputFile):
    with open(inputFile,'r') as f:
        read_data = f.readlines()
    return read_data
    
def writeAtoms(myfile,temp_data,atoms):
    for i in range(len(temp_data)):
        atype = int(temp_data[i][3])
        x = temp_data[i][0]
        y = temp_data[i][1]
        z = temp_data[i][2]
        myfile.write(str(i+1)+" "+str(atype)+" "+str(atoms['diameter'])+" "+str(atoms['density'])+
                     " "+str(x) +" "+str(y)+" "+str(z)+" "+"\n")
    
def generateAtoms(atoms, domainBox, safeBox):
    """Create a LAMMPS initial file
    
    Generate an evenly spaced atoms, inside the specified box
    
    """
    outfile = 'In_initial.in'
    domainBox = np.asarray(domainBox)
    safeBox = np.asarray(safeBox)
    bounds = (domainBox + safeBox)/2
    distance = atoms['diameter'] #distance between particles
    atype = 1
    nPartx = int(bounds[1]/distance-2)
    nParty = int(bounds[3]/distance-2)
    nPartz = int(bounds[5]/distance-2)
    temp_data = []
    count = 0
    for k in range(nPartx):
        for j in range(nParty):
            for i in range(nPartz):
                count +=1
                x = (k+1)*distance
                y = (j+1)*distance
                z = (i+1)*distance 
                temp_data.append([x, y, z, atype])
  
    with open(outfile, 'w') as myfile:
        myfile.write("sphere data\n\n")
        myfile.write(str(len(temp_data))+" atoms\n")
        myfile.write(str(atoms['nType'])+" atom types\n\n")
        myfile.write(" "+str(domainBox[0])+" "+str(domainBox[1])+" xlo xhi\n")
        myfile.write(" "+str(domainBox[2])+" "+str(domainBox[3])+" ylo yhi\n")
        myfile.write(" "+str(domainBox[4])+" "+str(domainBox[5])+" zlo zhi\n")
        myfile.write("\nAtoms\n\n")
        writeAtoms(myfile,temp_data,atoms)
    print('Created',outfile)

def freezeAtoms(inputFile,domainBox):
    """Change atom type to 2 (frozen)
    
    :params inputFile: LAMMPS input file
    
    """
    outfile = 'In_Frozen.in'
    with open(inputFile,'r') as f:
        read_data = f.read()
    read_data = read_data.replace(' 1 ',' 2 ')
    with open(outfile, 'w') as fileout:
        fileout.write(read_data)
    print('Created',outfile)

def activateAtoms(inputFile,atomType,box):
    """Change atom type for LAMMPS
    
    Change the type of all atoms inside the box to the desired value.
    Normally type 1 is for active atoms and type 2 are for frozen atoms
    
    :params inputFile: LAMMPS input file
    :params atomType: desired value of type inside the box
    :params box: lower and upper values for x, y and z
    
    """
    outfile = 'In_Active.in'
    read_data = loadFile(inputFile)
    box = np.asarray(box).astype(np.float)
    temp = []
    with open(outfile, 'w') as myfile:
        for i in range(0,10):
            myfile.write(read_data[i])
        myfile.write("\n")
        for i in range(11,len(read_data)):
            temp = read_data[i].split()
            temp = np.asarray(temp).astype(np.float)
            box = np.asarray(box).astype(np.float)
            if (temp[4] > box[0]) and (temp[4] < box[1]) and (temp[5] > box[2]) and (temp[5] < box[3]) and (temp[6] > box[4]) and (temp[6] < box[5]):
                myfile.write(str(int(temp[0]))+" "+str(int(atomType))+" "+str(temp[2])+" "+str(int(temp[3]))+
                             " "+str(temp[4]) +" "+str(temp[5])+" "+str(temp[6])+" "+"\n")
            else:
                myfile.write(str(int(temp[0]))+" "+str(int(temp[1]))+" "+str(temp[2])+" "+str(int(temp[3]))+
                             " "+str(temp[4]) +" "+str(temp[5])+" "+str(temp[6])+" "+"\n")
    print('Created',outfile)
    
def removeAtoms(inputFile, atoms, box):
    """Remove the atoms outside the safeBox
    
    :params inputFile: LAMMPS input file
    :params box: lower and upper values for x, y and z
    
    """
    outfile = 'In_Removed.in'
    read_data = loadFile(inputFile)
    temp = []
    temp_data = []

    for i in range(11,len(read_data)):
        temp = read_data[i].split()
        temp = list(map(float, temp))
        if (temp[4] > box[0]) and (temp[4] < box[1]) and (temp[5] > box[2]) and (temp[5] < box[3]) and (temp[6] > box[4]) and (temp[6] < box[5]):
            temp_data.append([temp[4], temp[5], temp[6], temp[1]])

    with open(outfile, 'w') as myfile:
        for i in range(10):
            if i == 2:
                myfile.write(str(len(temp_data))+" atoms\n")
            elif i == 3:
                myfile.write(str(atoms['nType'])+" atom types\n")
            else:
                myfile.write(read_data[i])
        writeAtoms(myfile,temp_data,atoms)  
    print('Created',outfile)
    
def ofToLammps(inputFile, atoms, domainBox):
    """Convert OpenFOAM file to LAMMPS
    
    It generates a LAMMPS compatible file
    
    :params inputFile: OpenFOAM 'positions' input file
    
    """
    outfile = 'In_OF.in'
    read_data = loadFile(inputFile)
    finalLine = len(read_data)-5
    temp_data = []

    for i in range(19,finalLine):
        modLine = read_data[i].replace('(','').replace(')','').split()
        temp_data.append([modLine[0],modLine[1],modLine[2],1])

    with open(outfile, 'w') as myfile:
        myfile.write("sphere data\n\n")
        myfile.write(str(len(temp_data))+" atoms\n")
        myfile.write(str(atoms['nType'])+" atom types\n\n")
        myfile.write(" "+str(domainBox[0])+" "+str(domainBox[1])+" xlo xhi\n")
        myfile.write(" "+str(domainBox[2])+" "+str(domainBox[3])+" xlo xhi\n")
        myfile.write(" "+str(domainBox[4])+" "+str(domainBox[5])+" xlo xhi\n")
        myfile.write("\nAtoms\n\n")
        writeAtoms(myfile,temp_data,atoms)
    print('Created',outfile)        
 
                             
def sumField(inputFile,sumField):
    read_data1 = loadFile(inputFile)
    read_data2 = loadFile(sumField)
    cellsFile = 'UbCells'
    read_data3 = loadFile(cellsFile)
    cells = int(read_data1[20])
    finalLine = len(read_data1)
    outfile = open('newUb','w')
    count = 0
    pointsList = []
    temp = []

    for i in range(0,22):
        outfile.write(str(read_data1[i])) 
    for i in range(22,finalLine):
        if read_data2[i] == ')\n':
            line = i
            outfile.write(')\n')
            break
        vortexField = read_data2[i].replace('(','').replace(')','').split()
        initialField = read_data1[i].replace('(','').replace(')','').split()
        cellsField = read_data3[i].replace('(','').replace(')','').split()
        arrayVortex = np.asarray(vortexField)
        arrayInitial = np.asarray(initialField)
        arrayCells = np.asarray(cellsField)
        arrayVortex = arrayVortex.astype(np.float)
        arrayInitial = arrayInitial.astype(np.float)
        cellsField = arrayCells.astype(np.int)
        
        if cellsField[0] == 999:
            result = arrayInitial + arrayVortex
            outfile.write('('+str(result[0])+' '+str(result[1])+' '+str(result[2])+')\n')
            count += 1
        else:
            outfile.write(str(read_data1[i]))
    for i in range(line+1,finalLine):
        outfile.write(str(read_data1[i]))

    outfile.close()
    print(count,"of",cells, "changed")	                             
