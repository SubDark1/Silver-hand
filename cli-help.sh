# Positional arguments
  target                Target URL to scan

# Optional arguments
  -h, --help           Show help message
  -t, --target         Target URL (required)
  -d, --depth          Crawling depth (default: 5)
  -o, --output         Output directory (default: ./reports)
  -v, --verbose        Verbose output
  
# Stealth options
  --stealth            Enable stealth mode
  --tor               Route through Tor
  --proxy-list FILE    Use proxy list from file
  --rotate-proxies     Enable proxy rotation
  --random-delay       Add random delays
  --max-threads N      Maximum threads (default: 100)

# WAF bypass options
  --waf-bypass         Enable WAF bypass
  --bypass-cloudflare  Bypass Cloudflare
  --bypass-akamai      Bypass Akamai
  --bypass-incapsula   Bypass Incapsula
  --obfuscate-payloads Obfuscate payloads

# Zero-day options
  --zero-day          Enable zero-day detection
  --zero-day-ml       Use ML for zero-day detection
  --fuzzing           Enable fuzzing
  --exploit-gen       Generate exploits
  --payloads N        Number of payloads (default: 10000)

# Output options
  --format FORMAT      Report format (html, pdf, json, csv)
  --language LANG      Report language (en, ar)
  --no-logo           Disable ASCII logo