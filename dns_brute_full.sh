dns_brute_full () {
        echo "[!] cleaning..."
        rm -f "$1.wordlist $1.dns_gen"
	echo "[!] making static world list..."
	curl -s https://wordlists-cdn.assetnote.io/data/manual/best-dns-wordlist.txt -o best-dns-wordlist.txt && curl -s https://wordlists-cdn.assetnote.io/data/manual/2m-subdomains.txt -o 2m-subdomains.txt && crunch 1 4 abcdefghijklmnopqrstuvwxyz1234567890 > 4-word.txt && cat best-dns-wordlist.txt 4-word.txt 2m-subdomains.txt | tr '[:upper:]' '[:lower:]' | sort -u > static-dns-brute.worldlist.txt && rm 2m-subdomains.txt 4-word.txt best-dns-wordlist.txt
	awk -v domain="$1" '{print $0"."domain}' "static-dns-brute.worldlist.txt" >> "$1.wordlist"
	rm static-dns-brute.worldlist.txt
	echo "[!] Start shuffledns static brute-force..."
	shuffledns -mode resolve -t 30 -silent -list $1.wordlist -d $1 -r ~/.resolver -m $(which massdns) | tee $1.dns_brute 2>&1 > /dev/null
	echo "[+] finished shuffledns Static, total $(wc -l $1.dns_brute) resolved..."
	echo "[!] running subfinder..."
	subfinder -d $1 -all -silent | dnsx -t 20 -retry 3 -r ~/.resolver -silent | anew $1.dns_brute 2>&1 > /dev/null
	echo "[+] finished, total $(wc -l $1.dns_brute) resolved..."
	echo "[!] Make word list ( dnsjen + altdns )"
	curl -s https://raw.githubusercontent.com/infosec-au/altdns/master/words.txt -o altdns-words.txt && curl -s https://raw.githubusercontent.com/ProjectAnte/dnsgen/master/dnsgen/words.txt -o dnsgen-words.txt && cat altdns-words.txt dnsgen-words.txt | sort -u > words-merged.txt && echo "2020\n2021\n2022\n2023\n2024\n2025" >> words-merged.txt && rm altdns-words.txt dnsgen-words.txt
	echo "[!] running DNSGen..."
	cat $1.dns_brute | dnsgen -w words-merged.txt - | egrep -v "^\." | egrep -v ".*\.\..*" | egrep -v ".*\-\..*" | egrep -v "^\-" | sort -u > $1.dns_gen 2>&1 > /dev/null
	echo "[+] finished with $(wc -l $1.dns_gen) words..."
	echo "[!] shuffledns dynamic brute-force on dnsgen results..."
	shuffledns -mode resolve -t 30 -silent -list $1.dns_gen -d $1 -r ~/.resolver -m $(which massdns) | anew $1.dns_brute 2>&1 > /dev/null
	echo "[+] finished, total $(wc -l $1.dns_brute) resolved..."
}
















