COUNTER=1
cd 4_base
mkdir -p postProcessing/planes
for d in postProcessing/surfaces/*/ ; do
    cp ${d}Ub_planeZ_35mm.raw postProcessing/planes/Ub_PlaneZ_35mm_${COUNTER}.raw
    COUNTER=$((COUNTER+1))
done
#cp postProcessing/surfaces/0.5/UbMean_planeZ_35mm.raw postProcessing/planes/UbMean_planeZ_35mm.raw
