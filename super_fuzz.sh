super_fuzz() {
  url="$1"
  filter="$2"
  local file="/root/test.txt"
  
  # Read and print each line of the file
  while IFS= read -r line; do
    ffuf -w "Desktop/world-list/$line" -u "$url/FUZZ" -mc all -c -H "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" "$filter"
    
    echo "################################################################"
  done < "$file"
}
