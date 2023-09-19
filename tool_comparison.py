# This script should just compare images in the Comparison folder

import os
from pathlib import Path

import cv2

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent

resources_dir = upper_dir / "PycharmProjects Resources" / "Adams Resources"

comparison_dir = resources_dir / "Comparison"

if not comparison_dir.exists():
    os.mkdir(comparison_dir)

count = 0

comparison_content_list = []

for file in comparison_dir.iterdir():
    comparison_content_list.append(file.name)

for image_file in comparison_content_list:

    count += 1

    source_file = os.path.join(comparison_dir, image_file)
    source_image = cv2.imread(source_file)

    source_shape = source_image.shape

    for compare_image_file in comparison_content_list[count:]:

        compare_file = os.path.join(comparison_dir, compare_image_file)
        compare_image = cv2.imread(compare_file)

        if source_shape == compare_image.shape:

            print(f"Source: {image_file} | Compare: {compare_image_file}")

            difference_image = cv2.absdiff(source_image, compare_image)

            rescale_width = int(source_shape[1] / 8)
            rescale_height = int(source_shape[0] / 8)

            difference_image = cv2.resize(difference_image, (rescale_width, rescale_height))

            b_channel, g_channel, r_channel = cv2.split(difference_image)

            if cv2.countNonZero(b_channel) == 0 and cv2.countNonZero(g_channel) == 0 and cv2.countNonZero(
                    r_channel) == 0:
                print(f"Source: {image_file} | Compare: {compare_image_file} | Same Image")

            cv2.imshow(f"Difference", difference_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
