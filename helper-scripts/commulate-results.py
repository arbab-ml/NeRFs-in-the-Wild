import csv
import json
import os


root_dir = "/work/mech-ai-scratch/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/lpips-validation-data-processed-5/evaluations"
csv_file = root_dir+"/results-lpips.csv"

# Initialize CSV file
with open(csv_file, 'w') as f:
    csv_writer = csv.writer(f)
    # headers = ["Model Name", "Number of Iterations", "Precision", "Recall", "F1 Score", "PSNR", "SSIM", "LPIPS", "Time Taken (s)"]
    headers = ["Model Name", "Number of Iterations", "PSNR", "SSIM", "LPIPS", "Time Taken (s)"]
    csv_writer.writerow(headers)

# Model rename dictionary
model_name_mapping = {
    "nerfacto": "NeRFacto",
    # "mipnerf": "MipNeRF",
    "tensorf": "TensoRF",
    "instant-ngp": "Instant-NGP"
}

for model in os.listdir(root_dir):
    if model in list(model_name_mapping.keys()): # we want to ignore the extra folders which are temp results from other experiments
        model_dir = os.path.join(root_dir, model)
        for iteration in os.listdir(model_dir):
            iteration_dir = os.path.join(model_dir, iteration)
            # console_log_path = os.path.join(iteration_dir, "console_log.txt") #EVAL
            psnr_json_path = os.path.join(iteration_dir, "psnr.json")
            time_taken_path = os.path.join(iteration_dir, "time_taken.txt")
            
            precision, recall, f1_score = "", "", ""
            psnr, ssim, lpips = "", "", ""
            time_taken = ""

            # with open(console_log_path, 'r') as f: #EVAL
            #     lines = f.readlines()
            #     for line in lines:
            #         if "precision :" in line:
            #             precision = "{:.2f}".format(float(line.split(":")[1].strip()) * 100)
            #         elif "recall :" in line:
            #             recall = "{:.2f}".format(float(line.split(":")[1].strip()) * 100)
            #         elif "f-score :" in line:
            #             f1_score = "{:.2f}".format(float(line.split(":")[1].strip()) * 100)

            if os.path.exists(psnr_json_path):
                with open(psnr_json_path, 'r') as f:
                    data = json.load(f)
                    results = data.get('results', data)
                    psnr = "{:.2f}".format(results.get('psnr', results.get('fine_psnr', '')))
                    ssim = "{:.2f}".format(results.get('ssim', results.get('fine_ssim', '')))
                    lpips = "{:.2f}".format(results.get('lpips', results.get('fine_lpips', '')))

            if os.path.exists(time_taken_path):
                with open(time_taken_path, 'r') as f:
                    time_taken = f.read().strip()

            #Sort the results by model name and then by number of iterations
            model = model.split("_")[0]

            # Write to CSV
            with open(csv_file, 'a') as f:
                csv_writer = csv.writer(f)
                # csv_writer.writerow([model, iteration, precision, recall, f1_score, psnr, ssim, lpips, time_taken])#EVAL
                csv_writer.writerow([model, iteration, psnr, ssim, lpips, time_taken])


print("Done compiling!")



# Define the column names
MODEL_NAME_COL = "Model Name"
ITERATIONS_COL = "Number of Iterations"
print(csv_file)

# Read the CSV file into a list of rows (as dictionaries)
with open(csv_file, 'r') as f:
    csv_reader = csv.DictReader(f)
    rows = list(csv_reader)

# Rename the model names based on the provided dictionary
for row in rows:
    row[MODEL_NAME_COL] = model_name_mapping.get(row[MODEL_NAME_COL], row[MODEL_NAME_COL])

# Sort the rows first by model name and then by the number of iterations
sorted_rows = sorted(rows, key=lambda x: (x[MODEL_NAME_COL], int(x[ITERATIONS_COL])))

# Write the sorted rows back to the CSV file
with open(csv_file, 'w', newline='') as f:
    fieldnames = csv_reader.fieldnames  # get the fieldnames from the csv_reader
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()  # Write the headers back
    csv_writer.writerows(sorted_rows)

print("CSV file sorted and model names updated!")
