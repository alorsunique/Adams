# This script should find similar images in the Create folder

import json
import os

import cv2
import numpy as np

project_dir = os.getcwd()
create_dir = os.path.join(project_dir, "Create")

JSON_comparison_dir = os.path.join("Comparison JSON.json")

if os.path.exists(JSON_comparison_dir):
    os.remove(JSON_comparison_dir)

json_file = open(JSON_comparison_dir, "w")

area = float(128 * 128)
threshold = float(0.01)

count = 0
threshold_count = 0

compare_pair_list = []

for image_file in os.listdir(create_dir):
    count += 1

    print(f"Working on image {count}")

    in_count = count

    source_file = os.path.join(create_dir, image_file)
    source_image = cv2.imread(source_file)

    for compare_image_file in os.listdir(create_dir)[count:]:
        in_count += 1

        compare_file = os.path.join(create_dir, compare_image_file)
        compare_image = cv2.imread(compare_file)

        difference_image = cv2.absdiff(source_image, compare_image)

        error = np.sum(difference_image ** 2)
        MSE = error / area
        RMSE = np.sqrt(MSE)

        if RMSE <= threshold:
            threshold_count += 1
            print(
                f"Source: {count} {image_file} | Compare: {in_count} {compare_image_file} | RMSE: {RMSE}  | {threshold_count}")
            compare_pair_list.append([image_file, compare_image_file])

json.dump(compare_pair_list, json_file)

json_file.close()
