#!/bin/bash

# Function to read the file and execute the command with replacements
run_command_with_replacements() {
    local file_path=$1
    local command_template=$2

    # Check if file exists
    if [[ ! -f "$file_path" ]]; then
        echo "Error: File '$file_path' not found."
        exit 1
    fi

    # Iterate over each line in the file
    while IFS= read -r line; do
        # Replace XXX in the command with the current line from the file
        local command="${command_template//XXX/$line}"
        
        # Run the modified command and capture the output
        echo "Running command: $command"
        eval "$command"
        echo "####------------------------------------------------####"
    done < "$file_path"
}

# Hardcoded file path (you can change this to your file's path)
file_path="/root/worldlist-file-path.txt"

# Check if a command template is provided as an argument
if [[ $# -ne 1 ]]; then
    echo "Usage: ./script.sh '<command>'"
    exit 1
fi

# Get the command template from the command-line arguments
command_template=$1

# Call the function to process the file and run the commands
run_command_with_replacements "$file_path" "$command_template"
