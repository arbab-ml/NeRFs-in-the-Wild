#!/bin/bash

# models=("nerfacto" "instant-ngp" "mipnerf")
# iterations=(1000 5000 10000 20000 30000)



models=("neus")
iterations=(507)
data_path="data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed"

for model in "${models[@]}"; do
  for iter in "${iterations[@]}"; do
    # echo all 
    echo "_________"
    echo $model $data_path $iter
    echo "_________"
    ./helper-scripts/train-and-evaluate-single.sh $model $data_path $iter



  done
done