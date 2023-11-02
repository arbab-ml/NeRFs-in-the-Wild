#!/bin/bash

models=("nerfacto")
iterations=(50 750 1450 2150 2850 3550 4250 4950 5650 6350 7050 7750 8450 9150 9850)




# models=("neus")
# iterations=(507)
data_path="data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple-polycam-images-processed"
experiment_name="vanilla"
for model in "${models[@]}"; do
  for iter in "${iterations[@]}"; do
    # echo all 
    echo "_________"
    echo $model $data_path $iter
    echo "_________"
    ./helper-scripts/train-and-evaluate-single.sh $model $data_path $iter $experiment_name

  done
done
