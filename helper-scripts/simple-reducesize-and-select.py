import os
import random

import cv2

src_dir = "data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single"
dst_dir = "data/nerfstudio/CCL-scanned-data-single/CCL-scannned-data-single-img-50-qual-90"

QUALITY = 90  # JPEG quality
NUM_IMAGES = 50  # Number of random images to select

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

all_files = [f for f in os.listdir(src_dir) if f.endswith('.png')]
selected_files = random.sample(all_files, min(NUM_IMAGES, len(all_files)))

for filename in selected_files:
    img = cv2.imread(os.path.join(src_dir, filename))
    cv2.imwrite(os.path.join(dst_dir, filename.replace('.png', '.jpg')), img, [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY])
