# gpt-repository-loader

`repo-loader` is a command-line tool that converts the contents of a Git repository into a text format, preserving the structure of the files and file contents. The generated output can be interpreted by AI language models, allowing them to process the repository's contents for various tasks, such as code review or documentation generation.


## Requirements

Ensure you have the following dependencies installed with Python:

```
pip install tiktoken
```

## Getting Started

To get started with `repo_loader`, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Clone or download the `gpt-prompts-helper` repository.
3. Navigate to the `repo_loader` directory inside the main repository via your terminal.
4. Execute `repo_loader` with the following command:

   ```bash
   python main.py /path/to/git/repository [-o /path/to/output_files/]
   ```
    Replace `/path/to/git/repository` with the path to the Git repository you want to process. Optionally, you can specify an output folder path with -o. If not specified, the default output folder is data/, with prompt.txt containing ititial prompt and repository_i.txt containing repository content.

5. The tool will generate repository_i.txt files containing the text representation of the repository. You can now use this file as input for AI language models or other text-based processing tasks.

## Testing
Some code is covered by unit tests, th eunittests are stored in ./tests/repo_loader folder


## License
This project is licensed under the MIT License - see the LICENSE file for details.
