# Simple scan
python3 silver.py -t https://example.com

# Advanced scan with all features
python3 silver.py -t https://example.com --stealth --tor --waf-bypass --zero-day

# Scan with custom options
python3 silver.py -t https://example.com -d 10 -o ./reports -v