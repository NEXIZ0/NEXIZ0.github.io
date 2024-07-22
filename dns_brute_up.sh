# Custom progress bar function
progress_bar() {
    local PROG_BAR_WIDTH=50
    local PROG_BAR_CHAR_DONE="#"
    local PROG_BAR_CHAR_TODO="-"
    local PROG_BAR_MSG="${2:-Progress}"

    local percent=$(bc <<< "scale=2; $1 * 100 / $2")
    local done=$(bc <<< "scale=0; $1 * $PROG_BAR_WIDTH / $2")
    local todo=$(bc <<< "$PROG_BAR_WIDTH - $done")

    local done_bar=$(printf "%${done}s" | tr ' ' "${PROG_BAR_CHAR_DONE}")
    local todo_bar=$(printf "%${todo}s" | tr ' ' "${PROG_BAR_CHAR_TODO}")

    printf "\r[${done_bar}${todo_bar}] ${PROG_BAR_MSG}: ${percent}%% (${1}/${2})"
}

# Main function
dns_brute_up() {
    echo "[!] Cleaning..."
    rm -f "$1.wordlist" "$1.dns_gen" "$1.dns_brute"

    echo "[!] Making static word list..."
    curl -s https://wordlists-cdn.assetnote.io/data/manual/best-dns-wordlist.txt -o best-dns-wordlist.txt
    curl -s https://wordlists-cdn.assetnote.io/data/manual/2m-subdomains.txt -o 2m-subdomains.txt
    crunch 1 4 abcdefghijklmnopqrstuvwxyz1234567890 > 4-word.txt
    cat best-dns-wordlist.txt 4-word.txt 2m-subdomains.txt | tr '[:upper:]' '[:lower:]' | sort -u > static-dns-brute.wordlist.txt
    rm 2m-subdomains.txt 4-word.txt best-dns-wordlist.txt

    awk -v domain="$1" '{print $0"."domain}' "static-dns-brute.wordlist.txt" >> "$1.wordlist"
    rm static-dns-brute.wordlist.txt

    echo "[!] Start shuffledns static brute-force..."
    total_lines=$(wc -l < "$1.wordlist")
    current_line=0

    while IFS= read -r line; do
        echo "$line" | shuffledns -mode resolve -t 30 -silent -list /dev/stdin -d "$1" -r ~/.resolver -m $(which massdns) >> "$1.dns_brute"
        ((current_line++))
        progress_bar $current_line $total_lines "Shuffledns Static Brute-Force"
    done < "$1.wordlist"

    echo ""
    echo "[+] Finished shuffledns static, total $(wc -l < "$1.dns_brute") resolved..."

    echo "[!] Running subfinder..."
    subfinder -d "$1" -all -silent | dnsx -t 20 -retry 3 -r ~/.resolver -silent | anew "$1.dns_brute" > /dev/null
    echo "[+] Finished, total $(wc -l < "$1.dns_brute") resolved..."

    echo "[!] Make word list (dnsgen + altdns)"
    curl -s https://raw.githubusercontent.com/infosec-au/altdns/master/words.txt -o altdns-words.txt
    curl -s https://raw.githubusercontent.com/ProjectAnte/dnsgen/master/dnsgen/words.txt -o dnsgen-words.txt
    cat altdns-words.txt dnsgen-words.txt | sort -u > words-merged.txt
    echo -e "2020\n2021\n2022\n2023\n2024\n2025" >> words-merged.txt
    rm altdns-words.txt dnsgen-words.txt

    echo "[!] Running DNSGen..."
    total_lines=$(wc -l < "$1.dns_brute")
    current_line=0

    cat "$1.dns_brute" | while IFS= read -r line; do
        echo "$line" | dnsgen -w words-merged.txt - | egrep --color=auto -v "^\." | egrep --color=auto -v ".*\.\..*" | egrep --color=auto -v ".*\-\..*" | egrep --color=auto -v "^\-" | sort -u >> "$1.dns_gen"
        ((current_line++))
        progress_bar $current_line $total_lines "DNSGen Generation"
    done

    echo ""
    echo "[+] Finished with $(wc -l < "$1.dns_gen") words..."

    echo "[!] Shuffledns dynamic brute-force on dnsgen results..."
    total_lines=$(wc -l < "$1.dns_gen")
    current_line=0

    while IFS= read -r line; do
        echo "$line" | shuffledns -mode resolve -t 30 -silent -list /dev/stdin -d "$1" -r ~/.resolver -m $(which massdns) | anew "$1.dns_brute" > /dev/null
        ((current_line++))
        progress_bar $current_line $total_lines "Shuffledns Dynamic Brute-Force"
    done < "$1.dns_gen"

    echo ""
    echo "[+] Finished, total $(wc -l < "$1.dns_brute") resolved..."

    # Compare word list with resolved domains
    echo "[!] Analyzing results..."
    comm -12 <(sort "$1.wordlist") <(sort "$1.dns_brute") > "$1.resolved_from_list"
    comm -23 <(sort "$1.dns_brute") <(sort "$1.wordlist") > "$1.brute_forced"

    resolved_count=$(wc -l < "$1.resolved_from_list")
    brute_forced_count=$(wc -l < "$1.brute_forced")
    total_resolved=$(wc -l < "$1.dns_brute")

    echo "Total words in original list: $(wc -l < "$1.wordlist")"
    echo "Total resolved words: $total_resolved"
    echo "Resolved words from original list: $resolved_count"
    echo "Brute-forced words: $brute_forced_count"
    echo "Proportion of brute-forced words: $(awk "BEGIN {print ($brute_forced_count / $total_resolved) * 100}")%"

    # Clean up
    rm "$1.wordlist" "$1.dns_gen" words-merged.txt "$1.resolved_from_list" "$1.brute_forced"
}
