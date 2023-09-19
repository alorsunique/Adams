# This script should rename edits
# Both PNG and JPG are supported


import os
import time
from datetime import datetime
from pathlib import Path

from exif import Image

# This setup the directory required for the code

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent

resources_dir = upper_dir / "PycharmProjects Resources" / "Adams Resources"

input_dir = resources_dir / "Input"

if not input_dir.exists():
    os.mkdir(input_dir)

# This section should perform a preliminary renaming.

img_count = 0

for image_file in input_dir.iterdir():
    print(f"Preliminary Renaming: {image_file.name}")

    file_handle = os.path.splitext(image_file.name)[1]

    time_filter = datetime.now()
    time_filter = time_filter.strftime("%H%M%S")
    img_count += 1

    new_img_name = f"{img_count}{time_filter}{file_handle}"
    new_img_name = input_dir / new_img_name

    os.rename(image_file, new_img_name)

# The actual renaming of the edited photos are done here

img_count = 0
same_img_count = 0

for image_file in input_dir.iterdir():

    file_handle = os.path.splitext(image_file.name)[1]

    print(f"Current Image Modified: {image_file.name}")

    source_file = image_file

    # In here, the type of file is considered
    # For PNG, no EXIF so the modification time is used
    # For JPG, EXIF is first checked before proceeding

    # Checks for PNG here

    if file_handle == ".png":

        modification_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(source_file)))

        datetime_chunk = modification_time.split(" ")
        date_chunk = datetime_chunk[0].split(":")
        time_chunk = datetime_chunk[1].split(":")
        rename_date = ""
        rename_time = ""
        for chunk in date_chunk:
            rename_date += chunk
        for chunk in time_chunk:
            rename_time += chunk

        new_name = f"Edit_{rename_date}_{rename_time}{file_handle}"

    # JPG is taken here

    else:

        image_handle = open(source_file, 'rb')

        image_object = Image(image_handle)

        image_handle.close()

        # EXIF check is done here

        if image_object.has_exif:

            # Image might have EXIF but has no datetime entry. Check is done here

            if image_object.get("datetime") == None:

                modification_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(source_file)))

                datetime_chunk = modification_time.split(" ")
                date_chunk = datetime_chunk[0].split(":")
                time_chunk = datetime_chunk[1].split(":")
                rename_date = ""
                rename_time = ""
                for chunk in date_chunk:
                    rename_date += chunk
                for chunk in time_chunk:
                    rename_time += chunk

            else:

                datetime_chunk = image_object.datetime.split(" ")
                date_chunk = datetime_chunk[0].split(":")
                time_chunk = datetime_chunk[1].split(":")
                rename_date = ""
                rename_time = ""
                for chunk in date_chunk:
                    rename_date += chunk
                for chunk in time_chunk:
                    rename_time += chunk

            # Now software used in creating will be checked

            if image_object.get("software") == None:
                new_name = f"Edit_{rename_date}_{rename_time}{file_handle}"
            else:
                software = image_object.software
                software = software.replace(" ", "_")
                new_name = f"Edit_{rename_date}_{rename_time}_{software}{file_handle}"

        else:

            modification_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(source_file)))

            datetime_chunk = modification_time.split(" ")
            date_chunk = datetime_chunk[0].split(":")
            time_chunk = datetime_chunk[1].split(":")
            rename_date = ""
            rename_time = ""
            for chunk in date_chunk:
                rename_date += chunk
            for chunk in time_chunk:
                rename_time += chunk

            new_name = f"Edit_{rename_date}_{rename_time}{file_handle}"

    new_img_dir = input_dir / new_name

    # This section checks for duplicates
    if new_img_dir.exists():
        print("Image Existing. Renaming Same Images")
        while True:
            same_img_count += 1
            name_split_tup = os.path.splitext(new_name)

            same_new_name = f"{name_split_tup[0]}_{same_img_count}{name_split_tup[1]}"
            same_dir = input_dir / same_new_name
            if not same_dir.exists():
                new_img_dir = same_dir
                break
        os.rename(source_file, new_img_dir)
        same_img_count = 0
    else:
        os.rename(source_file, new_img_dir)

    img_count += 1
