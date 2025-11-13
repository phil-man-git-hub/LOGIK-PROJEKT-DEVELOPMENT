import tiktoken
import os
import json
from datetime import datetime

def count_tokens_in_repo(repo_path):
    encoding = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0
    breakdown_by_extension = {}
    breakdown_by_directory = {}

    # Directories to ignore
    ignore_dirs = ['.git', '.venv', '__pycache__', 'node_modules', 'scripts', '.ai-context']
    # File extensions to ignore (e.g., binary files, images)
    ignore_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar', '.gz', '.bin']

    for root, dirs, files in os.walk(repo_path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Determine the top-level directory for breakdown
        relative_root = os.path.relpath(root, repo_path)
        if relative_root == '.':
            current_top_dir = '.'
        else:
            current_top_dir = relative_root.split(os.sep)[0]

        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in ignore_extensions:
                continue

            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tokens = len(encoding.encode(content))
                    total_tokens += tokens

                    # Update breakdown by extension
                    breakdown_by_extension[file_extension] = breakdown_by_extension.get(file_extension, 0) + tokens

                    # Update breakdown by top-level directory
                    breakdown_by_directory[current_top_dir] = breakdown_by_directory.get(current_top_dir, 0) + tokens

            except Exception as e:
                # print(f"Error reading {filepath}: {e}") # Uncomment for debugging file read errors
                pass # Silently skip unreadable files

    return total_tokens, breakdown_by_extension, breakdown_by_directory

def update_token_estimate_json(repo_path, total_tokens, breakdown_by_extension, breakdown_by_directory):
    json_file_path = os.path.join(repo_path, 'token-estimate.json')
    
    data = []
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list): # Ensure it's a list
                    data = []
        except json.JSONDecodeError:
            data = [] # Handle malformed JSON

    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_tokens": total_tokens,
        "breakdown_by_extension": breakdown_by_extension,
        "breakdown_by_directory": breakdown_by_directory
    }
    data.append(new_entry)

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    repo_root = os.getcwd() # Assumes script is run from repo root or adjusted path
    
    print(f"Counting tokens in: {repo_root}")
    total, by_ext, by_dir = count_tokens_in_repo(repo_root)
    update_token_estimate_json(repo_root, total, by_ext, by_dir)
    
    print(f"\nTotal tokens counted: {total:,}")
    print(f"Breakdown by extension: {by_ext}")
    print(f"Breakdown by top-level directory: {by_dir}")
    print(f"Results appended to token-estimate.json")
