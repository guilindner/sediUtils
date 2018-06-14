# sediUtils
utils to use with OpenFOAM and sediFoam (LAMMPS)

the file **config.py** should be used to adjust the simulation parameter like:
- quantity of particle types
- particle diameter and optionally the gaussian distribution
- particle density
- domainBox, where the simulation happens
- safeBox, where the particles will be kept after trimming
- activeBox, where the active particles box is defined, freezing the rest

## examples
generate initial file with evenly spaced particles:

```
python sediUtils.py -g 
```
output: *In_initialPython.in*
***

convert OpenFOAM lagrangian positions file to LAMMPS file:
```
python sediUtils.py -c -i positions
```
output: *In_OF.in*
***

Remove unnecessary particles and keep the atoms inside safeBox:
```
python sediUtils.py -r -i In_OF.in
```
output: *In_Removed.in*
***

Freeze all particles:
```
python sediUtils.py -f In_Removed.in
```
output: *In_Frozen.in*
***

Activate the atoms inside activeBox:
```
python sediUtils.py -a -i In_Frozen.in
```
output: *In_Active.in*
***

Add the OpenFOAM velocity from file U to the velocity field Ub, using the setField to define a box:
```
python sediUtils.py -i Ub -s U
```

---
