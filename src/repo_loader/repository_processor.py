import os
import glob
import sys
import fnmatch
import tiktoken

def get_ignore_list(ignore_file_path):
    ignore_list = []
    with open(ignore_file_path, 'r') as ignore_file:
        for line in ignore_file:
            line = line.strip()
            if line.startswith('#'):
                continue

            if line.endswith('/'):
                line += '*'
            if sys.platform == "win32":
                line = line.replace("/", '\\')
            
            ignore_list.append(line)
    return ignore_list


def should_ignore(file_path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def get_token_count(string, model_name='gpt-4'):
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(string))


def process_prompt_file(data_path, output_path):

    prompt_filename = 'prompt.txt'
    target_prompt_path = os.path.join(output_path, prompt_filename)

    if not os.path.exists(target_prompt_path):
        source_prompt_path = os.path.join(data_path, prompt_filename)
        if os.path.exists(source_prompt_path):
            with open(source_prompt_path, 'r') as source_file:
                content = source_file.read()
            with open(target_prompt_path, 'w') as target_file:
                target_file.write(content)
        else:
            print(f"Source prompt file not found at {source_prompt_path}")
    else:
        print(f"Prompt file already exists at {target_prompt_path}")    

def write_to_output(output_file, relative_path, content):
    output_file.write("-" * 4 + "\n")
    output_file.write(f"{relative_path}\n")
    output_file.write(f"{content}\n")
    output_file.write("!" + "-" * 4 + "\n")

def process_repository(repo_path, ignore_list, output_path, output_file_prefix='repository_', max_tokens=4000):
    
    def get_output_file_path(output_path, output_file_prefix, file_number):
        return os.path.join(output_path, f"{output_file_prefix}{file_number}.txt")

    def delete_files_with_pattern(output_path, output_file_prefix):
        # Create the search pattern
        search_pattern = os.path.join(output_path, f"{output_file_prefix}*.txt")

        # Use glob to get all matching files
        matching_files = glob.glob(search_pattern)

        # Delete each matching file
        for file_path in matching_files:
            os.remove(file_path)
            print(f"Deleted: {file_path}")

    delete_files_with_pattern(output_path,output_file_prefix)

    current_output_file_number = 1
    current_tokens_count = 0

    output_file = open(get_output_file_path(output_path, output_file_prefix, current_output_file_number), 'w')
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, repo_path)
            if should_ignore(relative_file_path, ignore_list):
                continue
            print(relative_file_path)    

            with open(file_path, 'r', errors='ignore') as file:
                contents = file.read()

            section_size = get_token_count(contents) + 10
            if current_tokens_count + section_size > max_tokens:
                output_file.close()
                current_output_file_number += 1
                current_tokens_count = 0
                output_file = open(get_output_file_path(output_path, output_file_prefix, current_output_file_number), 'w')
            
            write_to_output(output_file, relative_file_path, contents)
            current_tokens_count += section_size
    output_file.close()