# sediUtils
utils to use with OpenFOAM and sediFoam (LAMMPS)

## examples
generate initial file, with evenly spaced particles on specific box (x=0.2, y=0.03, z=0.02):

```
python sediUtils.py -c 0.2 0.03 0.02
```

---

change the atoms to type 3 if they are inside the box xlo=0.003 xhi=0.5 ylo=0.0 yhi=0.5 zlo=0.0 zhi=0.5 :
```
python sediUtils.py -i In_initial.in -a 3 -b 0.003 0.5 0.0 0.5 0.0 0.5
```

---

keep the atoms inside the box xlo=0.003 xhi=0.5 ylo=0.0 yhi=0.5 zlo=0.0 zhi=0.5 :
```
python sediUtils.py -i In_initial.in -k 1 -b 0.003 0.5 0.0 0.5 0.0 0.5
```

---

Add the velocity from file U to the velocity field Ub, using the setField to define a box:
```
python sediUtils.py -i Ub -s U
```

---
