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
    
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payloads = [
        "nexiz%22", "nexiz%2522", 'nexiz%27', "nexiz%2527",
        "nexiz%3C", "nexiz%253C", "<%=901*1100%>", "%7B%7B901*1100%7D%7D", "%24%7B901*1100%7D", "%40%28901*1100%29", "%24%7B%7B901*1100%7D%7D", "%23%7B901*1100%7D"
    ]
    
    keywords = ["nexiz'", 'nexiz"', "nexiz<", "991100"]
    
    try:
        with open(parameters_file, 'r') as file:
            parameters = file.readlines()
        
        for param in parameters:
            param = param.strip()
            progress_bar = tqdm(payloads, desc=f"Checking {param}", unit="request", colour='green')
            found_any = False
            count = 0

            # Check GET requests with payloads
            for payload in progress_bar:
                url = f"{base_url}&{param}={payload}"
                response = requests.get(url, headers=header)
                
                if any(keyword in response.text for keyword in keywords):
                    found_any = True
                    count += 1
                    found_urls.append(url)
                    progress_bar.set_postfix(found="YES", refresh=True)
                    progress_bar.set_description(f"Found {param}", refresh=True)
                time.sleep(1.5)
            
            # Additional checks with 'test' and 'nexiz' parameters
            test_url = f"{base_url}&{param}=test&{param}=nexiz"
            response = requests.get(test_url, headers=header)
            if "nexiz" in response.text:
                for payload in payloads:
                    url = f"{base_url}&{param}=test&{param}={payload}"
                    response = requests.get(url, headers=header)
                    
                    if any(keyword in response.text for keyword in keywords):
                        found_any = True
                        count += 1
                        found_urls.append(url)
                        progress_bar.set_postfix(found="YES", refresh=True)
                        progress_bar.set_description(f"Found {param}", refresh=True)
                    time.sleep(1.5)
            
            # Check POST requests with payloads
            for payload in payloads:
                data = {param: payload}
                response = requests.post(base_url, headers=headers, data=data)
                if any(keyword in response.text for keyword in keywords):
                    found_any = True
                    count += 1
                    found_urls.append(f"POST: {data}")
                    progress_bar.set_postfix(found="YES", refresh=True)
                    progress_bar.set_description(f"Found {param}", refresh=True)
                time.sleep(1.5)
                
            datas = {param: ['test', 'nexiz']}
            response = requests.post(base_url, headers=headers, data=datas)
            if "nexiz" in response.text:
                for payload in payloads:
                    dataz = {param: ['test', payload]}
                    response = requests.post(base_url, headers=headers, data=dataz)
                    if any(keyword in response.text for keyword in keywords):
                        found_any = True
                        count += 1
                        found_urls.append(f"POST: {dataz}")
                        progress_bar.set_postfix(found="YES", refresh=True)
                        progress_bar.set_description(f"Found {param}", refresh=True)
                    time.sleep(1.5)
                
            if found_any:
                print(f"Found: {param} {count}")
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
    
    except requests.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
