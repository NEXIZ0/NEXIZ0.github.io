import sys
import os
import requests
import time

def print_colored_progress(iteration, total, prefix='', suffix='', length=50, fill='█', color_code=''):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{color_code}{prefix} |{bar}| {percent}% {suffix}\033[0m')
    sys.stdout.flush()

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <base_url> <parameters_file>")
        return
    
    base_url = sys.argv[1]
    parameters_file = sys.argv[2]
    
    if not os.path.isfile(parameters_file):
        print(f"The file '{parameters_file}' does not exist.")
        return
    
    results = []  # List to store results
    
    try:
        with open(parameters_file, 'r') as file:
            parameters = file.readlines()
        
        total_params = len(parameters)
        param_count = 0
        
        # Print initial progress bar (default color)
        print_colored_progress(0, 1, prefix='Progress:', suffix='Complete', length=50, color_code='\033[0m')
        print()  # Move to the next line after the progress bar
        
        for param in parameters:
            param = param.strip()
            
            # List of values to try (not encoded)
            values = [
                "nexiz%22",
                "nexiz%2522",
                'nexiz%27',
                "nexiz%2527",
                "nexiz%3C",
                "nexiz%253C"
                ]
            
            value_count = 0
            total_values = len(values)
            
            for value in values:
                value_count += 1
                url = f"{base_url}&{param}={value}"
                
                response = requests.get(url)
                
                found_any = False  # Flag to check if any keyword is found in the response
                for keyword in ["nexiz'", 'nexiz"', "nexiz<"]:
                    if keyword in response.text:
                        found_any = True
                        break
                
                if found_any:
                    results.append(f"\033[92mFound: {url}\n\033[0m")
                    color_code = '\033[92m'  # Green color for found result
                else:
                    continue  # Skip appending for not found results
                
                # Calculate progress
                progress = (param_count * total_values + value_count) / (total_params * total_values)
                print_colored_progress(progress, 1, prefix='Progress:', suffix='Complete', length=50, color_code=color_code)
                time.sleep(1)  # Delay before next request
            
            param_count += 1
            print()  # Separate different parameters with a blank line for clarity
            time.sleep(1)  # Delay before processing next parameter
        
        # Print all results at the end
        print("\n\n===== All Results =====\n")
        for result in results:
            print(result)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
  
