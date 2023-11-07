#!/bin/bash

# models=("nerfacto" "instant-ngp" "mipnerf")
# iterations=(1000 5000 10000 20000 30000)
models=("instant-ngp" "nerfacto")
iterations=(30000)


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
done

# what is different in the reconstruction of plants and tanks and temples?
# 1. the number of images
# 2. the number of points in the point cloud
# 3. the number of iterations
# 4. the number of rays
# 5. the number of samples per ray
