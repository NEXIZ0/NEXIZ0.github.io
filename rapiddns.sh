rapiddns() {
  domain="$1"
  tmp_file="list.tmp"
  tmp_file2="list2.tmp"

  fetch_total() {
    curl -s "https://rapiddns.io/subdomain/$domain?page=2" \
      -H "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" \
      | grep -Ei "Total:" \
      | sed "s/<span style=\"color: #39cfca; \">//g" \
      | egrep -Eio ">.*<" \
      | cut -d ":" -f2 \
      | sed "s/<\/span><//g" \
      | sed "s/ //g"
  }

  total=$(fetch_total)
  result=$(echo "$total / 100" | bc)

  if [ "$result" -eq 0 ]; then
    total=$(fetch_total)
    result=$(echo "$total / 100" | bc)
  fi

  if [ "$result" -ne 0 ]; then
    result=$(echo "$result + 1" | bc)
  fi

  # Loop through the number of pages
  for i in $(seq 1 "$result")
  do
    curl -s "https://rapiddns.io/subdomain/$domain?page=$i" \
      -H "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" >> "$tmp_file"
    sleep 5
  done

  # Extract and filter results
  awk -F'</?td>' '{ for(i=2; i<=NF; i+=2) print $i }' "$tmp_file" | grep -Ei "$domain$" | sort -u | anew "$tmp_file2"
  grep -oP 'href="\K[^"]*' "$tmp_file" | cut -d "/" -f 3 | sed "s/#result//g" | grep -Ei "$domain$" | sort -u | anew "$tmp_file2"

  # Clean up temporary files
  rm "$tmp_file"
  rm "$tmp_file2"
}
