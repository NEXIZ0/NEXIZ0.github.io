import os
import subprocess

def super_fuzz(url, filter_option):
    file_path = "/root/test.txt"

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return 1

    # Read and process each line of the file
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Ensure line is not empty
            if line:
                # Ensure the file from the list exists before running ffuf
                if os.path.isfile(line):
                    cmd = [
                        'ffuf', '-w', line, '-u', f"{url}/FUZZ", '-mc', 'all', '-c',
                        '-H', 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                        filter_option
                    ]
                    subprocess.run(cmd)
                    print("#############--------------------------------########")
                else:
                    print(f"Warning: wordlist file not found for '{line}'")
