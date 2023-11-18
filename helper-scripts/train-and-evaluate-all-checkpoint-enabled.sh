#!/bin/bash

#WARNING: RUN ALL THE ITERATIONS TOGETHER. DO NOT INTERRUPT THE SCRIPT.
# FOR INDEPENDENT RUNS US SIMPLE ONE WITHOUT CHECKPOINTS ENABLED INSTEAD 

# models=("nerfacto" "instant-ngp" "mipnerf")
models=( "nerfacto")
iterations=(100 200 500 1000 2000 5000 10000)


# Save a flag "None" in a file named previous_run.txt in current directory after deleting the file first
rm previous_run.txt
echo "None" > previous_run.txt


# data_path="data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple-polycam-images-processed"
data_path="data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed"

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