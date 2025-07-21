#!/bin/bash

echo $"hello"

source activate base
conda activate methyldackel
path="/path_to_bam_files/mrkdup/"
outdir="/path_to_output/Methylkit/"
echo $path
echo $outdir
for files in "${path}"/*.bam; do
        outfile=$(basename $files ".mrkdup.bam")
        echo $outfile
        #for bedgraph file
        #MethylDackel extract --maxVariantFrac 0.251 --minOppositeDepth 4 \
        #--mergeContext --minDepth 8 ${path}/BosVos.fasta ${files} \
        #-o ${outdir}${outfile}
        
        # for methylkit file
        MethylDackel extract --maxVariantFrac 0.251 --minOppositeDepth 4 \
        --minDepth 4 --methylKit ${path}/BosVos.fasta ${files} \
        -o ${outdir}${outfile}
done
