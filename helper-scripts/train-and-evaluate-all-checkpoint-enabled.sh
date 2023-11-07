#!/bin/bash

# models=("nerfacto" "instant-ngp" "mipnerf")
# iterations=(1000 5000 10000 20000 30000)
models=("instant-ngp" "nerfacto")
iterations=(30000)

# Save a flag "None" in a file named previous_run.txt in current directory after deleting the file first
rm previous_run.txt
echo "None" > previous_run.txt


# models=("neus")
# iterations=(507)
# data_path="data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple-polycam-images-processed"
data_path="data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed"

for model in "${models[@]}"; do
  for iter in "${iterations[@]}"; do
    # echo all 
    echo "_________"
    echo $model $data_path $iter
    echo "_________"
    ./helper-scripts/train-and-evaluate-single.sh $model $data_path $iter



  done
  #resetting back to None after each model
  echo "None" > previous_run.txt
done