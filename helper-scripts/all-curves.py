#Iterating thorough all
import os

root_dir = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scanned-data-multiple-polycam-images-processed/evaluations"

output_folder = "helper-scripts/all-curves-multiple"

# Check if the output folder exists, if not create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


for model in os.listdir(root_dir):
    model_dir = os.path.join(root_dir, model)
    for iteration in os.listdir(model_dir):
        iteration_dir = os.path.join(model_dir, iteration, "evaluation")
        # copy the file (ending with _modified.pdf) to the output folder
        for file_name in os.listdir(iteration_dir):
            if file_name.endswith("_modified.pdf"):
                file_path = os.path.join(iteration_dir, file_name)
                output_image_name = f"{model}-{iteration}-{file_name}"
                output_image_path = os.path.join(output_folder, output_image_name)
                os.system(f"cp {file_path} {output_image_path}")
print("Processing completed!")
