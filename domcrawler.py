import sys
import re
import httpx
from tqdm import tqdm
from urllib.parse import urlparse

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0"
TLDS = (
    '.com', '.org', '.net', '.gov', '.edu', '.mil', '.int', '.biz', '.info', '.io', 
    '.co', '.uk', '.ca', '.au', '.jp', '.de', '.fr', '.it', '.cn', '.ru', '.br', 
    '.us', '.mx', '.es', '.in', '.kr', '.nl', '.se', '.ch', '.at', '.no', '.dk', 
    '.fi', '.be', '.pt', '.nz', '.sa', '.za', '.ar', '.cl', '.hu', '.ir', '.cz', 
    '.pl', '.gr', '.sg', '.hk', '.tw', '.my', '.th', '.vn', '.id', '.ph'
)

def read_domains(file_path):
    """Reads a list of domains from a file."""
    try:
        with open(file_path, 'r') as file:
            return [domain.strip() for domain in file.readlines()]
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def fetch_url_content(url):
    """Fetches content from the URL following the specified sequence."""
    headers = {'User-Agent': USER_AGENT, 'Referer': url}

    try:
        # 1) HTTP/1.1 on HTTPS
        with httpx.Client(http2=False) as client:
            response = client.get(url, headers=headers, timeout=5, follow_redirects=True)
            response.raise_for_status()
            return response.text
    except httpx.RequestError:
        pass

    try:
        # 2) HTTP/1.1 on HTTP
        url_http = url.replace("https://", "http://")
        headers['Referer'] = url_http
        with httpx.Client(http2=False) as client:
            response = client.get(url_http, headers=headers, timeout=5, follow_redirects=True)
            response.raise_for_status()
            return response.text
    except httpx.RequestError:
        pass

    try:
        # 3) HTTP/2 on HTTPS
        with httpx.Client(http2=True) as client:
            response = client.get(url, headers=headers, timeout=5, follow_redirects=True)
            response.raise_for_status()
            return response.text
    except httpx.RequestError:
        pass

    try:
        # 4) HTTP/2 on HTTP
        with httpx.Client(http2=True) as client:
            response = client.get(url_http, headers=headers, timeout=5, follow_redirects=True)
            response.raise_for_status()
            return response.text
    except httpx.RequestError as e:
           a = f"Failed to fetch {url}: {e}"

    return ""

def search_domains(content):
    """Searches for domains in the provided content."""
    pattern = r'([\w-]+(\.[\w-]+)+)'
    return re.findall(pattern, content)

def contains_unwanted_word(domain):
    """Checks if the domain contains the word 'google', 'facebook', or 'yahoo' in the host."""
    parsed_url = urlparse(f"https://{domain}")
    host = parsed_url.netloc
    return 'google' in host or 'facebook' in host or 'yahoo' in host

def main(file_path):
    domains = read_domains(file_path)
    all_valid_domains = set()

    for domain in tqdm(domains, desc="Processing domains", colour="green"):
        url = f"https://{domain}"
        content = fetch_url_content(url)
        if content:
            found_domains = search_domains(content)
            if found_domains:
                valid_domains = {match[0] for match in found_domains if match[0].endswith(TLDS)}
                all_valid_domains.update(valid_domains)
    
    sorted_valid_domains = sorted(all_valid_domains)
    filtered_domains = [domain for domain in sorted_valid_domains if not contains_unwanted_word(domain)]
    
    for valid_domain in filtered_domains:
        print(valid_domain)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 example.py subdomain.txt")
    else:
        file_path = sys.argv[1]
        main(file_path)
                        
