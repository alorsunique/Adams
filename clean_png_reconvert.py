# This script should fix the PNG edits that were converted to JPG
# A proper EXIF and proper time tag will be added to the files
# Use for edits with the format Edit_{date}_{time}_ConvertedPNG

import os
import shutil
import time
from datetime import datetime
from pathlib import Path

from exif import Image

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent

resources_dir = upper_dir / "PycharmProjects Resources" / "Adams Resources"

input_dir = resources_dir / "Input"
create_dir = resources_dir / "Create"

if create_dir.exists():
    shutil.rmtree(create_dir)
os.mkdir(create_dir)

if not input_dir.exists():
    os.mkdir(input_dir)

for image_file in input_dir.iterdir():
    print(image_file.name)

    image_handle = open(image_file, 'rb')

    image_object = Image(image_handle)

    image_handle.close()

    # In this part of the script, the date and time are extracted

    filename_split = image_file.name.split("_")

    date_chunk = filename_split[1]
    time_chunk = filename_split[2]

    date_chunk = f"{date_chunk[:4]}:{date_chunk[4:6]}:{date_chunk[6:]}"
    time_chunk = f"{time_chunk[:2]}:{time_chunk[2:4]}:{time_chunk[4:]}"

    datetime_info = f"{date_chunk} {time_chunk}"
    datetime_object = datetime.strptime(datetime_info, '%Y:%m:%d %H:%M:%S')

    print(f"Date Time Info: {datetime_info} | Date Time Object: {datetime_object}")

    creation_time = time.mktime(datetime_object.timetuple())
    modification_time = time.mktime(datetime_object.timetuple())

    image_object["software"] = "Converted PNG"
    image_object["datetime_original"] = datetime_info
    image_object["datetime"] = datetime_info

    print(f"EXIF: {image_object.has_exif} | EXIF List: {image_object.list_all()}")

    create_image_dir = create_dir / f"New_{image_file.name}"

    create_handle = open(create_image_dir, 'wb')

    create_handle.write(image_object.get_file())

    create_handle.close()

    os.utime(create_image_dir, (creation_time, modification_time))
