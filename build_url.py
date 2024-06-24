import sys
import os
import requests
import time  # Import the time module

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <base_url> <parameters_file>")
        return
    
    base_url = sys.argv[1]
    parameters_file = sys.argv[2]
    
    if not os.path.isfile(parameters_file):
        print(f"The file '{parameters_file}' does not exist.")
        return
    
    try:
        with open(parameters_file, 'r') as file:
            parameters = file.readlines()
            
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
            for value in values:
                url = f"{base_url}&{param}={value}"  # Construct the URL with the parameter and its value
                #print(f"Checking URL: {url}")
                
                # Make a GET request to the URL
                response = requests.get(url)
                
                # Check each variation of "nexiz" in the response content
                found = False
                for keyword in ["nexiz'", 'nexiz"', "nexiz<"]:
                    if keyword in response.text:
                        found = True
                        break
                
                if found:
                    print(f"Found : {url}")
                    # You can also print additional details like response status code, etc.
                    #print(f"Response Status Code: {response.status_code}")
                    print(f"Response Content: {response.text}")
                
                time.sleep(2)  # Introduce a 2-second delay between requests
            
            print()  # Separate different parameters with a blank line for clarity
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
