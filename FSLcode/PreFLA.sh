#!/bin/bash
# FSL script for processing BIDS data, preprocessing and first-level analysis for each run of each subject
# Author: Zhao Peng-geng
# Platform: Windows Subsystem for Linux, Ubuntu 22.04
# FSL version: 6.0.7.13

#运行此命令前需要先运行Timing.sh脚本，生成high和low两个条件下的文件
bids="/research/Re/Painlearning/data"

subjlist=$(ls -1 $bids | grep '^sub-' | sed -e 's/\/.*//')

for subj in $subjlist; do
    echo "===> Starting processing of $subj"
    cd /research/Re/Painlearning/data/$subj
    if [ ! -f anat/${subj}_T1w_brain.nii.gz ]; then
        echo "Skull-stripped brain not found, using bet with a fractional intensity threshold of 0.5"
        bet2 anat/${subj}_T1w.nii.gz \
            anat/${subj}_T1w_brain.nii.gz -f 0.5
    fi

    runlist=$(ls -1 func/${subj}_task-tsl_run-*.nii | grep -oP 'run-[^_]*')
    for run in $runlist; do
        filename="${subj}-${run}.fsf"
        cp /research/Re/Painlearning/code/FSLcode/design.fsf "$filename"
        sed -i "s|sub-06|${subj}|g" "$filename"
        sed -i "s|run-01|${run}|g" "$filename"
        echo "---Starting feat for ${run} of ${subj}..."
        feat "$filename"
        echo "---Finished feat for ${run} of ${subj}"
    done
    echo "-Finishing processing all runs of $subj!"

    cd /research/Re/Painlearning/data
done
echo "All processing completed."