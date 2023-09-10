# This script should downscale the image and convert it to grayscale for faster preliminary filtering

import os
import shutil

from pathlib import Path

import cv2

project_dir = Path.cwd()

current_dir = project_dir
current_dir = current_dir.parent.parent

resources_dir = current_dir / "PycharmProjects Resources" / "Adams Resources"

input_dir = resources_dir / "Input"
create_dir = resources_dir / "Create"

if create_dir.exists():
    shutil.rmtree(create_dir)
os.mkdir(create_dir)

count = 0

new_height = 128
new_width = 128

for image_file in input_dir.iterdir():
    count += 1
    print(f"{count} | {image_file.name}")

    source_image = cv2.imread(str(image_file))
    source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

    resize_image = cv2.resize(source_image, (new_width, new_height))

    resize_dir = create_dir / image_file.name
    cv2.imwrite(str(resize_dir), resize_image)
    cv2.destroyAllWindows()
