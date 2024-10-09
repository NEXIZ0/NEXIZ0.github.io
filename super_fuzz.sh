super_fuzz() {
  url="$1"
  filter="$2"
  local file="/root/test.txt"
  
  # Check if the file exists
  if [[ ! -f "$file" ]]; then
    echo "File not found: $file"
    return 1
  fi

  # Read and print each line of the file
  while IFS= read -r line || [[ -n "$line" ]]; do
    # Ensure line is not empty and the file from the list exists before running ffuf
    if [[ -n "$line" && -f "Desktop/world-list/$line" ]]; then
      ffuf -w "Desktop/world-list/$line" -u "$url/FUZZ" -mc all -c -H "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" $filter
      echo "#############--------------------------------########"
    else
      echo "Warning: wordlist file not found for '$line'"
    fi
  done < "$file"
}
