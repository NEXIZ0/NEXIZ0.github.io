import sys
import os
import requests
import time
from tqdm import tqdm

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <base_url> <parameters_file>")
        return
    
    base_url = sys.argv[1]
    parameters_file = sys.argv[2]
    
    if not os.path.isfile(parameters_file):
        print(f"The file '{parameters_file}' does not exist.")
        return
    
    found_urls = []  # List to store URLs where keyword was found
    
    try:
        with open(parameters_file, 'r') as file:
            parameters = file.readlines()
            
        for param in parameters:
            param = param.strip()
            
            values = [
                "nexiz%22",
                "nexiz%2522",
                'nexiz%27',
                "nexiz%2527",
                "nexiz%3C",
                "nexiz%253C"
            ]
            
            progress_bar = tqdm(values, desc=f"Checking {param}", unit="request", colour='green')
            found_any = False

            for value in progress_bar:
                url = f"{base_url}&{param}={value}"
                response = requests.get(url)
                
                for keyword in ["nexiz'", 'nexiz"', "nexiz<"]:
                    if keyword in response.text:
                        found_any = True
                        found_urls.append(url)  # Store the URL where keyword was found
                        progress_bar.set_postfix(found="YES", refresh=True)
                        progress_bar.set_description(f"Found {param}", refresh=True)
                        break
                time.sleep(1)
            
            urlX = f"{base_url}&{param}=test&{param}=nexiz"
            responseX = requests.get(urlX)
            if "nexiz" in responseX.text:
                for value in values:
                    urlZ = f"{base_url}&{param}=test&{param}={value}"
                    responseZ = requests.get(urlZ)
                
                    for keyword in ["nexiz'", 'nexiz"', "nexiz<"]:
                        if keyword in responseZ.text:
                            found_any = True
                            found_urls.append(urlZ)  # Store the URL where keyword was found
                            progress_bar.set_postfix(found="YES", refresh=True)
                            progress_bar.set_description(f"Found {param}", refresh=True)
                            break
                    time.sleep(1)
            
            if found_any:
                print(f"Found: {param}")
            else:
                print(f"Not Found: {param}")
            
            time.sleep(1)  # Delay before processing next parameter
        
        # Print all found URLs
        if found_urls:
            print("\nFound URLs:")
            for url in found_urls:
                print(url)
        else:
            print("\nNo URLs found.")
       
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
