import json
import os

project_dir = os.getcwd()
input_dir = os.path.join(project_dir, "Input")

JSON_comparison_dir = os.path.join("True Comparison JSON.json")
json_file = open(JSON_comparison_dir, "r")
positive_pair_list = json.load(json_file)
json_file.close()

count = 0

processed_pair_list = []
processed_group_list = []

for pair in positive_pair_list:

    count += 1

    if pair not in processed_pair_list:

        group_list = []

        processed_pair_list.append(pair)

        for entry in pair:
            if entry not in group_list:
                group_list.append(entry)

        for next_pair in positive_pair_list[count:]:
            if next_pair not in processed_pair_list:

                first_set = set(group_list)
                second_set = set(next_pair)

                if len(first_set.intersection(second_set)) > 0:

                    for entry in next_pair:
                        if entry not in group_list:
                            group_list.append(entry)

                    processed_pair_list.append(next_pair)

        processed_group_list.append(group_list)

deletable_count = 0

for entry in processed_group_list:

    deletable_count += len(entry)-1

    for image_file in entry[1:]:

        image_dir = os.path.join(input_dir, image_file)

        if os.path.exists(image_dir):
            os.remove(image_dir)

print(f"Deletable Count: {deletable_count}")