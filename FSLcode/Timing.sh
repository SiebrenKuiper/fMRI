#!/bin/bash

subjlist=("sub-06" "sub-07" "sub-08" "sub-09" "sub-10" "sub-11" "sub-13" "sub-14" "sub-15" "sub-16" "sub-17" "sub-18" "sub-19" "sub-20" "sub-21" "sub-22" "sub-23" "sub-24" "sub-25" "sub-26" "sub-27" "sub-28" "sub-29" "sub-30" "sub-31" "sub-32" "sub-33" "sub-36" "sub-37" "sub-38" "sub-39" "sub-41" "sub-42" "sub-43" "sub-44")
runlist=("run-01" "run-02" "run-03" "run-04" "run-05")

process_run() {
    local run=$1
    local condition=$2
    local condition_name=$3
    
    local filename="${subj}_task-tsl_${run}_events.tsv"
    
    if [ -f "$filename" ]; then
        cat "$filename" | awk -v cond="$condition" '{if ($3==cond) {print $1, $2, "1"}}' > "${condition_name}_${run}.txt"
    else
        echo "File not found: $filename"
    fi
}

for subj in "${subjlist[@]}"; do
    cd "/research/Re/Painlearning/data/$subj/func"
    
    for run in "${runlist[@]}"; do
        process_run "$run" "high" "high"
        process_run "$run" "low" "low"
    done
    
    cd ../../
done