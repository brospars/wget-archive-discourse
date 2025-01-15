import os
import re
import shutil

# Define the directory to search in
directory = 'course/static/'

# Define the regex patterns and their replacements for search and replace
patterns = [
    (r'%3Fpage=([^"]*).html', r'-page-\1.html'),
    (r'%3Fno_definitions=[^0-9]*([0-9]+).html', r'-page-\1.html'),
    (r'%3Fv([^"]*)', r''),
    (r'%3F__ws([^"]*)', r'')
]

# List of text file extensions to process
text_extensions = {'.txt', '.html', '.xml', '.json', '.md', '.js', '.css'}

# Function to perform search and replace in a file
def search_and_replace(file_path, patterns):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Recursively traverse the directory and apply search and replace
for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        _, ext = os.path.splitext(file_path)
        if ext.lower() in text_extensions:
            search_and_replace(file_path, patterns)

print("Search and replace completed.")

# Function to rename files based on patterns
def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = file_path

            # Rename files ending with ?v=X
            if re.search(r'\?v=[0-9]*$', file):
                new_file_path = re.sub(r'\?v=[0-9]*$', '', file_path)

            # Rename files ending with ?__ws=xxx
            elif re.search(r'\?__ws=[^"]*$', file):
                new_file_path = re.sub(r'\?__ws=[^"]*$', '', file_path)

            # Rename paginated files latest?page=1.html => latest-page-1.html
            elif re.search(r'\?page=[0-9]*.html$', file):
                new_file_path = re.sub(r'\?page=([0-9]*).html$', r'-page-\1.html', file_path)

            # Remove files with no_definitions duplicates
            elif re.search(r'\?no_definitions=true.*\.html$', file):
                os.remove(file_path)
                continue

            if new_file_path != file_path:
                shutil.move(file_path, new_file_path)
                print(f"Renamed: {file_path} to {new_file_path}")

# Rename files in the directory
rename_files(directory)

print("File renaming completed.")
