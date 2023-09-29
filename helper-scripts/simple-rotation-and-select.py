import os
import random

import cv2

src_dir = "data/nerfstudio/CCL-plant-for-evaluation/Jul18at3-17PM-poly/keyframes/images"
dst_dir = "data/nerfstudio/CCL-plant-for-evaluation/Jul18at3-17PM-poly/keyframes/images-rotated-half"
select_percent = 0.8

os.makedirs(dst_dir, exist_ok=True)

img_list = [img_name for img_name in os.listdir(src_dir) if img_name.endswith('.jpg')]
selected_imgs = random.sample(img_list, int(len(img_list) * select_percent))

for img_name in selected_imgs:
    img = cv2.imread(os.path.join(src_dir, img_name))
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(os.path.join(dst_dir, img_name), rotated_img)
