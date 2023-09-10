# This script should rename photos with EXIF taken from phones and cameras

import os
import shutil
from datetime import datetime

from exif import Image

project_dir = os.getcwd()
input_dir = os.path.join(project_dir, "Input")
output_dir = os.path.join(project_dir, "Output")

# Initialize the folders involved

if not os.path.exists(input_dir):
    os.mkdir(input_dir)
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)

# This section should check if image has EXIF

for image_file in os.listdir(input_dir):

    image_in_dir = os.path.join(input_dir, image_file)

    image_handle = open(image_in_dir, 'rb')

    try:
        image_object = Image(image_handle)
        jpg_type = True
    except Exception:
        jpg_type = False
        print("Not JPG")

    image_handle.close()

    if jpg_type and image_object.has_exif:
        image_out_dir = os.path.join(output_dir, image_file)
        shutil.move(image_in_dir, image_out_dir)

# This section should perform a preliminary renaming.

img_count = 0

for image_file in os.listdir(output_dir):
    source_file = os.path.join(output_dir, image_file)

    print(f"Preliminary Renaming: {image_file}")

    file_handle = os.path.splitext(image_file)[1]

    time_filter = datetime.now()
    time_filter = time_filter.strftime("%H%M%S")
    img_count += 1

    new_img_name = f"{img_count}{time_filter}{file_handle}"
    new_img_name = os.path.join(output_dir, new_img_name)

    os.rename(source_file, new_img_name)

# This section should now process the images and renames them accordingly

img_count = 0
same_img_count = 0

for image_file in os.listdir(output_dir):
    source_file = os.path.join(output_dir, image_file)

    print(f"Current Renaming: {image_file}")

    file_handle = os.path.splitext(image_file)[1]

    image_handle = open(source_file, 'rb')

    image_object = Image(image_handle)

    image_handle.close()

    datetime_chunk = image_object.datetime.split(" ")
    date_chunk = datetime_chunk[0].split(":")
    time_chunk = datetime_chunk[1].split(":")

    rename_date = ""
    rename_time = ""

    for chunk in date_chunk:
        rename_date += chunk
    for chunk in time_chunk:
        rename_time += chunk

    new_img_name = f"{rename_date}_{rename_time}_{image_object.model}{file_handle}"
    new_img_name = os.path.join(output_dir, new_img_name)

    # This section checks for duplicates
    if os.path.exists(new_img_name):
        print("Image Existing. Renaming Same Images")
        while True:
            same_img_count += 1
            same_new_name = f"{rename_date}_{rename_time}_{image_object.model}_{same_img_count}{file_handle}"
            same_dir = os.path.join(output_dir, same_new_name)
            if not os.path.exists(same_dir):
                new_img_name = same_dir
                break
        os.rename(source_file, new_img_name)
        same_img_count = 0
    else:
        os.rename(source_file, new_img_name)

    img_count += 1

print(f"Total Images Renamed: {img_count}")