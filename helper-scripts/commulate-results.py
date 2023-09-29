import csv
import json
import os

csv_file = "results-28Sep.csv"

# Initialize CSV file
with open(csv_file, 'w') as f:
    csv_writer = csv.writer(f)
    headers = ["Model Name", "Number of Iterations", "Precision", "Recall", "F1 Score", "PSNR", "SSIM", "LPIPS", "Time Taken (s)"]
    csv_writer.writerow(headers)

root_dir = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/evaluations"

for model in os.listdir(root_dir):
    model_dir = os.path.join(root_dir, model)
    for iteration in os.listdir(model_dir):
        iteration_dir = os.path.join(model_dir, iteration)
        console_log_path = os.path.join(iteration_dir, "console_log.txt")
        psnr_json_path = os.path.join(iteration_dir, "psnr.json")
        time_taken_path = os.path.join(iteration_dir, "time_taken.txt")
        
        precision, recall, f1_score = "", "", ""
        psnr, ssim, lpips = "", "", ""
        time_taken = ""

        with open(console_log_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "precision :" in line:
                    precision = "{:.2f}".format(float(line.split(":")[1].strip()) * 100)
                elif "recall :" in line:
                    recall = "{:.2f}".format(float(line.split(":")[1].strip()) * 100)
                elif "f-score :" in line:
                    f1_score = "{:.2f}".format(float(line.split(":")[1].strip()) * 100)

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
            csv_writer.writerow([model, iteration, precision, recall, f1_score, psnr, ssim, lpips, time_taken])

print("Done!")



