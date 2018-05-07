#!/bin/bash
set -e

mx=20
my=20
mz=10

flow=0.2
vortexR=0.01
vortexS=50
settleTime=0.5
flowTime=0.5
convectTime=0.5

baseDir=baseTest
baseDirVortex=baseTestVortex
dir1=1_$baseDir
dir2=2_$baseDir
dir3=3_$baseDir
dir4=4_$baseDir
UTILS=~/OpenFOAM/sediUtils
#################### 1 #################### 
# 1 - create settling case dir 
cp -r $baseDir $dir1
cd $dir1

# define domain e mesh
sed -i "s/100 100 50/$mx $my $mz/" constant/polyMesh/blockMeshDict

# define simulation time
sed -i "s/^endTime.*/endTime         $settleTime;/" system/controlDict

# generate particles
echo "1 - generating particles"
###python3 $UTILS/sediUtils.py -g

# generate mesh and run simulation
# TODO:change blockMesh coordinates and refinment
echo "1 - blockMesh"
###blockMesh > log.blockMesh
echo "1 - lammpsFoam"
###lammpsFoam > log.lammpsFoam
qsub thor1.pbs


#check if the final file has been generated
while ! [ -f $settleTime/Ub ];
do
    echo "waiting lammpsFoam to finish"
    sleep 60
done 
cd ..

#################### 2 #################### 
# 2 - create normal flow case dir
cp -r $dir1 $dir2
cd $dir2

# define simulation time
sed -i "s/^endTime.*/endTime         $flowTime;/" system/controlDict

# convert settled particles into LAMMPS format 
python3 $UTILS/sediUtils.py -c -i $settleTime/lagrangian/defaultCloud/positions
rm -rf 0.25 0.5

# prepare thor file
mv thor1.pbs thor2.pbs
sed -i "s/GL_1_02/GL_2_$mx/" thor2.pbs

# remove unnecessary particles
python3 $UTILS/sediUtils.py -r -i In_OF.in

# freeze all particles
python3 $UTILS/sediUtils.py -f -i In_Removed.in
sed -i "s/In_initial.in/In_Frozen.in/" in.lammps

# define simulation time
sed -i "s/endTime         1;/endTime         $flowTime;/" system/controlDict

# set flow velocity
sed -i "s/.*Ubar.*/Ubar            Ubar [0 1 -1 0 0 0 0] ($flow 0 0); \/\/ average velocity in the channel/" constant/transportProperties

# run simulation
# TODO:change blockMesh coordinates and refinment
echo "2 - lammpsFoam"
#lammpsFoam > log.lammpsFoam
qsub thor2.pbs

#check if the final file has been generated
while ! [ -f $flowTime/Ub ];
do
    echo "waiting lammpsFoam to finish"
    sleep 60
done 

cd ..

#################### 3 #################### 
# 3 - create vortex case dir
cp -r $baseDirVortex $dir3
cd $dir3

# define domain and mesh
sed -i "s/100 100 50/$mx $my $mz/" constant/polyMesh/blockMeshDict

# define vortex properties
sed -i "s/.*speed=50;.*/            \"speed=$vortexS;\"/" system/fvOptions
sed -i "s/.*radius=0.01;.*/            \"radius=$vortexR;\"/" system/fvOptions

# generate mesh and run simulation
# TODO:change blockMesh coordinates and refinment
echo "3 - blockMesh"
blockMesh > log.blockMesh
echo "3 - simpleFoam"
simpleFoam > log.simpleFoam


#prepare fields
setFields > log.setFields
cd ..

#################### 4 #################### 
# 4 - create convective case dir
cp -r $dir2 $dir4
cd $dir4
rm -rf 0.25 0.5

# define simulation time
sed -i "s/^endTime.*/endTime         $convectTime;/" system/controlDict

# prepare thor file
mv thor2.pbs thor4.pbs
sed -i "s/GL_2_$mx/GL_4_$mx/" thor4.pbs
echo "foamToVTK -fields '(alpha p Q Ua Ub)'" >> thor4.pbs

# generate combined velocity
cp ../$dir3/0/UbCells .
echo "4 - combining velocity fields"
python3 $UTILS/sediUtils.py -s ../$dir3/1/U -i ../$dir2/$flowTime/Ub
mv newUb 0/Ub


# define simulation time
sed -i "s/endTime         1;/endTime         $convectTime;/" system/controlDict 

# activate particles
python3 $UTILS/sediUtils.py -a -i In_Frozen.in
sed -i "s/In_Frozen.in/In_Active.in/" in.lammps

# run simulation
echo "4 - lammpsFoam"
#lammpsFoam > log.lammpsFoam
echo "4 - foamToVTK"
#foamToVTK > log.foamToVTK
qsub thor4.pbs
