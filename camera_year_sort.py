# This script should sort the entries in the output folder into their respective years
# Use this script to sort only camera photos. Edits are not taken into account

import os
import shutil

from exif import Image

project_dir = os.getcwd()
output_dir = os.path.join(project_dir, "Output")
sort_dir = os.path.join(project_dir, "Sorted Directory")

if not os.path.exists(sort_dir):
    os.mkdir(sort_dir)

count = 0

for image_file in os.listdir(output_dir):

    count += 1
    print(f"Current Count: {count} | {image_file}")

    source_file = os.path.join(output_dir, image_file)

    image_handle = open(source_file, 'rb')

    image_object = Image(image_handle)

    image_handle.close()

    datetime_chunk = image_object.datetime.split(" ")
    date_chunk = datetime_chunk[0].split(":")

    img_year = int(date_chunk[0])
    in_year = img_year - 2017

    season_folder = f"S{in_year}"

    move_folder = os.path.join(sort_dir, season_folder)
    if not os.path.exists(move_folder):
        os.mkdir(move_folder)

    shutil.move(source_file, move_folder)
