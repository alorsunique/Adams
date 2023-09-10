# This script should downscale the image and convert it to grayscale for faster preliminary filtering

import os
import shutil

import cv2

project_dir = os.getcwd()
input_dir = os.path.join(project_dir, "Input")
create_dir = os.path.join(project_dir, "Create")

if os.path.exists(create_dir):
    shutil.rmtree(create_dir)
os.mkdir(create_dir)

count = 0

new_height = 128
new_width = 128

for image_file in os.listdir(input_dir):
    count += 1
    print(f"{count} | {image_file}")

    source_file = os.path.join(input_dir, image_file)
    source_image = cv2.imread(source_file)
    source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

    resize_image = cv2.resize(source_image, (new_width, new_height))

    resize_dir = os.path.join(create_dir, image_file)
    cv2.imwrite(resize_dir, resize_image)
    cv2.destroyAllWindows()
