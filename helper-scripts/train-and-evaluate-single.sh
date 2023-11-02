#!/bin/bash
# THIS ONLY WORKS ON A100 GPU
set -e 
#Sample Run: ./train-and-evaluate-single.sh nerfacto /work/mech-ai/arbab/nerfstudio/data/nerfstudio/CCL-plant-for-evaluation/Jul18at3-17PM-poly-processed-rotated-half 10000
#Sample Run:  ./helper-scripts/train-and-evaluate-single.sh nerfacto data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple-processed-img-200 10000


# This assumes that the data is preprocessed already
# For example using: ns-process-data images --data data/nerfstudio/CCL-plant-for-evaluation/Jul18at3-17PM-poly/keyframes/images-rotated-half --output_dir data/nerfstudio/CCL-plant-for-evaluation/Jul18at3-17PM-poly-processed-rotated-half

#Sequential matching method (for videos) - also serves resources usage exception
# ns-process-data images --matching-method sequential --data data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90 --output_dir data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed

#Preprocessing command for 2nd scenario
# ns-process-data video --matching-method sequential --no-gpu  --num-frames-target 100 --data
#  data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple/IMG_0157.MOV --output_dir data/nerfstudio/CCL-scanned-data-multiple/CCL-scann
# ed-data-multiple-processed
# second scenario using polycam data
# ns-process-data polycam --data data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple-polycam/capture.zip --output_dir data/nerfstudio/CCL-scanned-data-multiple/CCL-scanned-data-multiple-polycam-processed
echo "Stargin"
# Variables
re_run_evaluation=true # This will rerun the evaluation scripts even if the model was already trained, by loading its relavent checkpoint
nerfstudio_main_directory=$(pwd)
model_name=$1 # nerfacto
data_path=$2 # /work/mech-ai/arbab/nerfstudio/data/nerfstudio/CCL-plant-for-evaluation/Jul18at3-17PM-poly-processed-rotated-half
training_iterations=$3 
# data_identifier="ccl-plant"
data_identifier=$(basename "$data_path")

tank_and_temples_main_directory=/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation
# redirecting all the console output to a file as well as console
output_directory_for_model_evaluation=${tank_and_temples_main_directory}/data/${data_identifier}/evaluations/${model_name}/${training_iterations}
mkdir -p ${output_directory_for_model_evaluation}
# if ${output_directory_for_model_evaluation}/config_for_export.txt exists, then skip the training 
if [ -f "${output_directory_for_model_evaluation}/config_for_export.txt" ]; then
  already_trained=1
else
  already_trained=0
fi

if [ "$already_trained" -eq 1 ] && [ "$re_run_evaluation" != true ]; then
exit 0
fi

# Modules and directory for training
source activate nerfstudio10
module load colmap
module load cuda
cd /work/mech-ai/arbab/NeRFs-in-the-Wild




if [ $already_trained -eq 0 ]; then
  SECONDS=0
  if [ "$model_name" = "nerfacto" ]; then
    ns-train $model_name --viewer.websocket-port 8008 --viewer.quit-on-train-completion True --data $data_path --max-num-iterations $training_iterations # previously it had prediction of normals but that's replaced by open3d
  else
    ns-train $model_name --viewer.websocket-port 8008 --viewer.quit-on-train-completion True --data $data_path --max-num-iterations $training_iterations
  fi
  duration=$SECONDS
  echo "$duration" > "${output_directory_for_model_evaluation}/time_taken.txt"
fi

# Point cloud export
latest_folder=$(ls -d /work/mech-ai/arbab/NeRFs-in-the-Wild/outputs/${data_path##*/}/$model_name/* | sort -r | head -n 1)
config_for_export="$latest_folder/config.yml"
echo $config_for_export
output_dir_pointcloud="$(pwd)/exports/pcd/${data_path##*/}/${model_name}"
#append above with working directory
bbox_min=(-1.0 -1.0 -1.0)
bbox_max=(1.0 1.0 1.0)
if [ $already_trained -eq 0 ]; then # Only training if it was not already trained
  case "$model_name" in
    "mipnerf")
      ns-export pointcloud --normal-method open3d --load-config $config_for_export --output-dir $output_dir_pointcloud --num-points 1000000 --remove-outliers True  --use-bounding-box True --bounding-box-min "${bbox_min[@]}" --bounding-box-max "${bbox_max[@]}" --rgb_output_name 'rgb_fine' --depth_output_name 'rgb_fine'
      ;;
    "instant-ngp")
      ns-export pointcloud --normal-method open3d --load-config $config_for_export --output-dir $output_dir_pointcloud --num-points 1000000 --remove-outliers True  --use-bounding-box True --bounding-box-min "${bbox_min[@]}" --bounding-box-max "${bbox_max[@]}"
      ;;
    "nerfacto")
      ns-export pointcloud --normal-method open3d --load-config $config_for_export --output-dir $output_dir_pointcloud --num-points 1000000 --remove-outliers True  --use-bounding-box True --bounding-box-min "${bbox_min[@]}" --bounding-box-max "${bbox_max[@]}" 
      ;;
  esac
fi


# if the model was already trained then the config_for_export.txt will give us the config_for_export variable
if [ $already_trained -eq 1 ]; then
  config_for_export=$(cat ${output_directory_for_model_evaluation}/config_for_export.txt)
fi

# Modules and directory for Evaluation
source activate tanksandtemples-eval-env2
cd /work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox

# Prerequisites: 
#1. Have the log file processed using command like: python convert_to_logfile.py /work/mech-ai/arbab/nerfstudio/data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed/colmap/sparse/0/ /work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/CCL-scannned-data-single-img-50-qual-90-processed_COLMAP_SfM.log /work/mech-ai/arbab/nerfstudio/data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90-processed/images/ COLMAP jpg
# -> things to be careful about: there should be a training / at the end of 0/ otherwise it will not work
# -> create teh folder for the log file before running the command


#2. Have ground truth pointcloud in /work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/ccl-plant/ccl-plant.ply

#3. Have alignment file: ccl-plant_trans.txt
#4. Have crop file: ccl-plant.json
#5. Add your threshold for dataset in scenes_tau_dict

# make this command generic: python run.py --dataset-dir data/ccl-plant --traj-path data/ccl-plant/ccl-plant_COLMAP_SfM.log --ply-path data/ccl-plant/ccl-plant-nerfacto.ply
cd evaluation

# If the model is already trained, then we don't need to copy the point cloud. Otherwise, we copy the point cloud 
if [ $already_trained -eq 0 ]; then 
cp "${output_dir_pointcloud}/point_cloud.ply" ${output_directory_for_model_evaluation}/point_cloud.ply
fi

python run.py \
  --dataset-dir ${tank_and_temples_main_directory}/data/${data_identifier} \
  --traj-path ${tank_and_temples_main_directory}/data/${data_identifier}/${data_identifier}_COLMAP_SfM.log \
  --ply-path ${output_directory_for_model_evaluation}/point_cloud.ply \
  &> ${output_directory_for_model_evaluation}/console_log.txt


# cp -r data/${data_identifier}/evaluation/* data/${data_identifier}/evaluations/${model_name}/${training_iterations}/
# rm -rf data/${data_identifier}/evaluation/*

## PSNR calculation, again activating the nerfstudio environment


cd $nerfstudio_main_directory
source activate nerfstudio10
ns-eval --load-config $config_for_export --output-path ${output_directory_for_model_evaluation}/psnr.json

#Save the value of variable config_for_export in a file inside the evaluation folder; This is also used as a flag for skipping the training
echo $config_for_export > ${output_directory_for_model_evaluation}/config_for_export.txt



