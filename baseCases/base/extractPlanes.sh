COUNTER=1
mkdir -p postProcessing/planes
for d in postProcessing/surfaces/*/ ; do
    cp ${d}Ub_planeZ_35mm.raw postProcessing/planes/Ub_PlaneZ_35mm_${COUNTER}.raw
    cp ${d}Ub_planeY_50mm.raw postProcessing/planes/Ub_PlaneY_50mm_${COUNTER}.raw
    cp ${d}alpha_planeY_50mm.raw postProcessing/planes/alpha_planeY_50mm_${COUNTER}.raw
    COUNTER=$((COUNTER+1))
done
#cp postProcessing/surfaces/0.5/UbMean_planeZ_35mm.raw postProcessing/planes/UbMean_planeZ_35mm.raw
