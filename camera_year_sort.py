# This script should sort the entries in the output folder into their respective years
# Use this script to sort only camera photos. Edits are not taken into account

import os
import shutil
from pathlib import Path

from exif import Image

project_dir = Path.cwd()

current_dir = project_dir
current_dir = current_dir.parent.parent

resources_dir = current_dir / "PycharmProjects Resources" / "Adams Resources"

output_dir = resources_dir / "Output"
sort_dir = resources_dir / "Sorted Directory"

if not sort_dir.exists():
    os.mkdir(sort_dir)

count = 0

for image_file in output_dir.iterdir():

    count += 1
    print(f"Current Count: {count} | {image_file.name}")

    image_handle = open(image_file, 'rb')

    image_object = Image(image_handle)

    image_handle.close()

    datetime_chunk = image_object.datetime.split(" ")
    date_chunk = datetime_chunk[0].split(":")

    img_year = int(date_chunk[0])
    in_year = img_year - 2017

    season_folder = f"S{in_year}"

    move_folder = sort_dir / season_folder
    if not move_folder.exists():
        os.mkdir(move_folder)

    shutil.move(image_file, move_folder)
