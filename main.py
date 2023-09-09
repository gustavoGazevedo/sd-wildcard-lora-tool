import os
import json
from itertools import combinations

def get_combinations(trained_word):
    combinations_list = []
    min = config_data["minimumNumberOfCombinations"]
    rang = len(trained_word) + 1
    if min != 0:
        rang = min + 1
    for r in range(1, rang):
        comb = combinations(trained_word , r)
        combinations_list.extend([", ".join(c) for c in comb])
    return combinations_list

# Function to read a .civitai.info file and return its contents as a JSON object
def read_civitai_info(file_path):
    try:
        with open(file_path, 'r') as civitai_info_file:
            civitai_info = json.load(civitai_info_file)
            trained_words = civitai_info.get("trainedWords", [])
            return trained_words
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON in '{file_path}': {e}")
        return []

# Function to scan the specified folders and their subfolders for .safetensor and .pt files
def scan_folders(whitelist, blacklist, subfolders):
    results = []
    
    def is_allowed_folder(folder):
        return folder not in blacklist
    
    for folder_path in whitelist:
        for root, dirs, files in os.walk(folder_path):
            if not subfolders and root != folder_path:
                break  # If subfolders are not allowed, skip subfolders
            folderName = ""
            if root != folder_path:
                folderName = os.path.basename(root)

            for file in files:
                file_name, file_extension = os.path.splitext(file)
                if file_extension in ('.safetensors', '.pt'):
                    file_path = os.path.join(root, file)
                    parent_folder = os.path.dirname(file_path)
                    
                    if is_allowed_folder(parent_folder):
                        civitai_info_path = os.path.join(parent_folder, f"{file_name}.civitai.info")
                        trained_words = get_combinations(read_civitai_info(civitai_info_path))
                        
                        if trained_words is not None:
                            result_item = {
                                "name": file_name,
                                "trained_words": trained_words,
                                "folder": folderName
                            }
                            results.append(result_item)

    return results


# def replace_unicode_comma(input_string):
#     return input_string.replace('\uff0c', ', ')

# Load the configuration data from the JSON file
config_file_path = 'config.json'
try:
    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print(f"Error: File '{config_file_path}' not found.")
    exit()
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse JSON in '{config_file_path}': {e}")
    exit()

# Get the folders configuration from the loaded data
whitelist = config_data["whitelist"]
blacklist = config_data["blacklist"]
subfolders = config_data["subfolders"]

# Scan the folders and collect the results
results = scan_folders(whitelist, blacklist, subfolders)

counter = 0

output_file_path = "wildcards/" + config_data["WildcardName"] + ".txt"

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for item in results:
        # print(item)

        for weight in config_data["weights"]:
            output_line = f"<lora:{item['name']}:{weight}>"
            counter += 1
            output_file.write(output_line + "\n")

            # Write trained words for this name and weight combination
            for trained_word in item["trained_words"]:
                # print(trained_word)
                line = f"{trained_word}, <lora:{item['name']}:{weight}>"
                output_file.write(line + "\n")
                counter += 1

if config_data["createWildcardForSubfolders"]:
    items_by_folder = {}

    for item in results:
        folder_name = item["folder"]
        if folder_name == "":
            break
        if folder_name not in items_by_folder:
            items_by_folder[folder_name] = []
        items_by_folder[folder_name].append(item)

    if len(items_by_folder) > 0:
        for folder_name, items in items_by_folder.items():
            folder_file_name = f"wildcards/{folder_name}.txt"

            with open(folder_file_name, "w", encoding='utf-8') as output_file:
                for item in items:
                    for weight in config_data["weights"]:
                        output_line = f"<lora:{item['name']}:{weight}>"
                        output_file.write(output_line + "\n")

                        # Write trained words for this name and weight combination
                        for trained_word in item["trained_words"]:
                            # print(trained_word)
                            line = f"{trained_word}, <lora:{item['name']}:{weight}>"
                            output_file.write(line + "\n")

print(f"Number of wildcards: {counter}")