import os
import random

import cv2

src_dir = "/work/mech-ai/arbab/NeRFs-in-the-Wild/data/nerfstudio/CCL-scanned-data-outdoor-stage2-low-height/CCL-scanned-data-outdoor-stage2-low-height"
dst_dir = "/work/mech-ai/arbab/NeRFs-in-the-Wild/data/nerfstudio/CCL-scanned-data-outdoor-stage2-low-height/CCL-scanned-data-outdoor-stage2-low-height-22"
select_percent = 1

os.makedirs(dst_dir, exist_ok=True)

img_list = [img_name for img_name in os.listdir(src_dir) if img_name.endswith('.jpg')]
selected_imgs = img_list
    # DISABLED RANDOM SAMPLING
# random.sample(img_list, int(len(img_list) * select_percent))

for img_name in selected_imgs:
    img = cv2.imread(os.path.join(src_dir, img_name))
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(os.path.join(dst_dir, img_name), rotated_img)
