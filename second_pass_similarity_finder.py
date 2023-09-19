# This script should use the results from the first pass to refine the similarities further

import json
import os
from pathlib import Path

import cv2

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent

resources_dir = upper_dir / "PycharmProjects Resources" / "Adams Resources"

input_dir = resources_dir / "Input"

JSON_comparison_dir = resources_dir / "Comparison JSON.json"
json_file = open(JSON_comparison_dir, "r")
compare_pair = json.load(json_file)
json_file.close()

true_JSON_comparison_dir = resources_dir / "True Comparison JSON.json"

if true_JSON_comparison_dir.exists():
    os.remove(true_JSON_comparison_dir)

json_file = open(true_JSON_comparison_dir, "w")

count = 0

positive_pairs = []

length_compare_pair = len(compare_pair)

for pair in compare_pair:

    count += 1

    print(f"Comparison Number: {count}/{length_compare_pair} | {pair}")

    source_file = os.path.join(input_dir, pair[0])
    compare_file = os.path.join(input_dir, pair[1])

    source_image = cv2.imread(source_file)
    compare_image = cv2.imread(compare_file)

    if source_image.shape == compare_image.shape:
        difference_image = cv2.subtract(source_image, compare_image)
        b_channel, g_channel, r_channel = cv2.split(difference_image)

        if cv2.countNonZero(b_channel) == 0 and cv2.countNonZero(g_channel) == 0 and cv2.countNonZero(r_channel) == 0:
            positive_pairs.append(pair)

print(f"Similar Pairs: {len(positive_pairs)}")

json.dump(positive_pairs, json_file)

json_file.close()
