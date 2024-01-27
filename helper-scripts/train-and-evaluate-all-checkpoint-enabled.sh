#!/bin/bash

#WARNING: RUN ALL THE ITERATIONS TOGETHER. DO NOT INTERRUPT THE SCRIPT.
# FOR INDEPENDENT RUNS US SIMPLE ONE WITHOUT CHECKPOINTS ENABLED INSTEAD 

# models=( "nerfacto" "instant-ngp" "tensorf")
# iterations=(100 200 400 800 1000 5000 10000 20000 30000 60000)

models=( "nerfacto")
iterations=(20001)



# Save a flag "None" in a file named previous_run.txt in current directory after deleting the file first
rm previous_run.txt
echo "None" > previous_run.txt


# data_path="data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple-polycam-images-processed"
# data_path="data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed"
data_path="data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed-alpha-channel"

# CCL-scannned-data-single-img-50-qual-90-processed-pixel-sampler
# data_path="/work/mech-ai-scratch/arbab/NeRFs-in-the-Wild/data/nerfstudio/CCL-scanned-data-outdoor-stage2-low-height/CCL-scanned-data-outdoor-stage2-low-height-processed"

for model in "${models[@]}"; do
  for iter in "${iterations[@]}"; do
    # echo all 
    echo "_________"
    echo $model $data_path $iter
    echo "_________"
    ./helper-scripts/train-and-evaluate-single-checkpoints-enabled.sh $model $data_path $iter


  done
  #resetting back to None after each model
  echo "None" > previous_run.txt
done