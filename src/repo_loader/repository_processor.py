import os
from utils import get_token_count, should_ignore

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