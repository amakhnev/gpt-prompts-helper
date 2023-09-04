import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path

from repository_processor import process_repository, process_prompt_file
from utils import get_ignore_list

def main():

    if len(sys.argv) < 2:
        print("Usage: python git_to_text.py /path/to/git/repository [-o /path/to/output_dir]")
        sys.exit(1)

    repo_path = sys.argv[1]
    if not os.path.exists(repo_path):
        print(f"Not existing repository path {repo_path}")
        sys.exit(1)
    repo_path = os.path.abspath(repo_path) 
           
    data_path = os.path.join(Path(__file__).parents[2],'data','repo_loader')
   
    output_path = os.path.join(data_path,'out')
    if "-o" in sys.argv:
        output_path = sys.argv[sys.argv.index("-o") + 1]
        
    if not os.path.exists(output_path):
        print(f"Not existing output path {output_path}")
        sys.exit(1)

    ignore_list = ['.git*', '.gptignore']

    ignore_file_path = os.path.join(repo_path,'.gitignore')
    if os.path.exists(ignore_file_path):
        ignore_list.extend(get_ignore_list(ignore_file_path))

    ignore_file_path = os.path.join(repo_path,'.gptignore')
    if os.path.exists(ignore_file_path):
        ignore_list.extend(get_ignore_list(ignore_file_path))

    ignore_file_path = os.path.join(data_path,'.gptignore')
    if os.path.exists(ignore_file_path):
        ignore_list.extend(get_ignore_list(ignore_file_path))


    process_prompt_file(data_path,output_path)

    process_repository(repo_path, ignore_list, output_path)

    print(f"Repository contents written to {output_path}.")
    
if __name__ == "__main__":
    main()
