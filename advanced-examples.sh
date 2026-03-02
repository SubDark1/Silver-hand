# Example 1: Basic scan with report
python3 silver.py -t https://example.com -o ./reports

# Example 2: Stealth scan with Tor and proxies
python3 silver.py -t https://example.com --stealth --tor --rotate-proxies

# Example 3: Zero-day hunting with ML
python3 silver.py -t https://example.com --zero-day --zero-day-ml --fuzzing

# Example 4: WAF bypass scan
python3 silver.py -t https://example.com --waf-bypass --obfuscate-payloads

# Example 5: Full power scan
python3 silver.py -t https://example.com --stealth --tor --waf-bypass --zero-day --exploit-gen -v

# Example 6: Scan with custom wordlist
python3 silver.py -t https://example.com -w ./wordlists/custom.txt

# Example 7: Distributed scanning
python3 silver.py -t https://example.com --distributed --node workers=10

# Example 8: Generate report only
python3 silver.py -t https://example.com --report-only --format pdf