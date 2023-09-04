import fnmatch
import sys
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
