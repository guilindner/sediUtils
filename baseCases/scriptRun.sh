#!/bin/bash
set -e
set -x

module load codes/openfoam/2.3.1
source ~/swak4Foam/prefs.sh

UTILS=~/sediUtils
configFile="$UTILS/config.py"
mx=$(cat $configFile | grep "^mx" | cut -d "=" -f 2)
my=$(cat $configFile | grep "^my" | cut -d "=" -f 2)
mz=$(cat $configFile | grep "^mz" | cut -d "=" -f 2)
flow=$(cat $configFile | grep "^flow" | cut -d "=" -f 2)
vortexR=$(cat $configFile | grep "^vortexR" | cut -d "=" -f 2)
vortexS=$(cat $configFile | grep "^vortexS" | cut -d "=" -f 2)
settleTime=$(cat $configFile | grep "^settleTime" | cut -d "=" -f 2)
flowTime=$(cat $configFile | grep "^flowTime" | cut -d "=" -f 2)
convectTime=$(cat $configFile | grep "^convectTime" | cut -d "=" -f 2)

baseDir=base
baseDirVortex=baseVortex

dir1=1_$baseDir
dir2=2_$baseDir
dir3=3_$baseDir
dir4=4_$baseDir

run1 () {
    # 1 - create settling case dir 
    cp -r $baseDir $dir1
    cd $dir1
    
    # define domain e mesh
    sed -i "s/mx my mz/$mx $my $mz/" constant/polyMesh/blockMeshDict
    
    # define simulation time
    sed -i "s/^endTime.*/endTime         $settleTime;/" system/controlDict
    
    # generate particles
    echo "1 - generating particles"
    python $UTILS/sediUtils.py -g
    
    # prepare thor file
    sed -i "s/GL_1_xx/GL_1_$mx/" thor1.pbs
    
    # TODO:change blockMesh coordinates and refinment
    #echo "1 - blockMesh"
    ###blockMesh > log.blockMesh
    #echo "1 - lammpsFoam"
    ###lammpsFoam > log.lammpsFoam
    echo "1 - launching simulation"
    qsub thor1.pbs
    
    
    #check if the final file has been generated
    while ! [ -f $settleTime/Ub ];
    do
        echo "1 - waiting lammpsFoam to finish"
        sleep 600
    done 
    cd ..
}

run2 () {
    # 2 - create normal flow case dir
    cp -r $dir1 $dir2
    cd $dir2
    
    # define simulation time
    sed -i "s/^endTime.*/endTime         $flowTime;/" system/controlDict
    sed -i "s/^writeInterval.*/writeInterval   $flowTime;/" system/controlDict
    
    # convert settled particles into LAMMPS format
    echo "2 - converting particles" 
    python $UTILS/sediUtils.py -c -i $settleTime/lagrangian/defaultCloud/positions
    
    rm -rf 0.* [1-9]*
    rm log*
    
    # perturb Ub velocity
    setFields > log.setFields
    python $UTILS/sediUtils.py -p -i 0/Ub
    mv newUb 0/Ub    
    
    # prepare thor file
    mv thor1.pbs thor2.pbs
    sed -i "s/GL_1_$mx/GL_2_$mx/" thor2.pbs
    sed -i "s/$dir1/$dir2/" thor2.pbs
    
    # remove unnecessary particles
    python $UTILS/sediUtils.py -r -i In_OF.in
    
    # freeze all particles
    python $UTILS/sediUtils.py -f -i In_Removed.in
    sed -i "s/In_initial.in/In_Frozen.in/" in.lammps
    
    # define simulation time
    sed -i "s/endTime         1;/endTime         $flowTime;/" system/controlDict
    
    # set flow velocity
    sed -i "s/.*Ubar.*/Ubar            Ubar [0 1 -1 0 0 0 0] ($flow 0 0);/" constant/transportProperties
    
    # run simulation
    # TODO:change blockMesh coordinates and refinment
    #echo "2 - lammpsFoam"
    #lammpsFoam > log.lammpsFoam
    echo "2 - launching simulation"
    qsub thor2.pbs
    
    #check if the final file has been generated
    while ! [ -f $flowTime/Ub ];
    do
        echo "2 - waiting lammpsFoam to finish"
        sleep 600
    done 
    
    cd ..
}

run3 () {
    # 3 - create vortex case dir
    cp -r $baseDirVortex $dir3
    cd $dir3
    
    # define domain and mesh
    sed -i "s/mx my mz/$mx $my $mz/" constant/polyMesh/blockMeshDict
    
    # define vortex properties
    sed -i "s/.*speed=xx;.*/            \"speed=$vortexS;\"/" system/fvOptions
    sed -i "s/.*radius=x.xx;.*/            \"radius=$vortexR;\"/" system/fvOptions
    
    # generate mesh and run simulation
    # TODO:change blockMesh coordinates and refinment
    echo "3 - blockMesh"
    blockMesh > log.blockMesh
    echo "3 - simpleFoam"
    simpleFoam > log.simpleFoam
    
    
    #prepare fields
    setFields > log.setFields
    cd ..
}

run4 () {
    # 4 - create convective case dir
    cp -r $dir2 $dir4
    cd $dir4
    rm -rf 0.* [1-9]*
    rm log*
    
    # define simulation time
    sed -i "s/^endTime.*/endTime         $convectTime;/" system/controlDict
    sed -i "s/^writeInterval.*/writeInterval   0.02;/" system/controlDict
    
    # prepare thor file
    mv thor2.pbs thor4.pbs
    sed -i "s/GL_2_$mx/GL_4_$mx/" thor4.pbs
    sed -i "s/2_base/4_base/" thor4.pbs
    #echo "Q" >> thor4.pbs
    #echo "foamToVTK -fields '(alpha p Q Ua Ub)' -allPatches" >> thor4.pbs
    
    # generate combined velocity
    cp ../$dir3/0/UbCells .
    echo "4 - combining velocity fields"
    python $UTILS/sediUtils.py -s ../$dir3/1/U -i ../$dir2/$flowTime/Ub
    mv newUb 0/Ub
    
    
    # define simulation time
    sed -i "s/endTime         1;/endTime         $convectTime;/" system/controlDict 
    
    # activate particles
    python $UTILS/sediUtils.py -a -i In_Frozen.in
    sed -i "s/In_Frozen.in/In_Active.in/" in.lammps
    
    # run simulation
    #echo "4 - lammpsFoam"
    #lammpsFoam > log.lammpsFoam
    #echo "4 - foamToVTK"
    #foamToVTK > log.foamToVTK
    echo "4 - launching simulation"
    qsub thor4.pbs
}

if [ -f $dir1/$settleTime/Ub ]; then
    echo "case 1 already simulated"
else
    run1
fi

if [ -f $dir2/$flowTime/Ub ]; then
    echo "case 2 already simulated"
else
    run2
fi
if [ -f $dir3/1/U ]; then
    echo "case 3 already simulated"
else
    run3
fi
if [ -f $dir4/$convectTime/Ub ]; then
    echo "case 4 already simulated"
else
    run4
fi
echo "script finished"
