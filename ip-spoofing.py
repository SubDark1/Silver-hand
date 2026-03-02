# Use original client IP via headers
headers = {
    'X-Forwarded-For': '127.0.0.1',
    'X-Real-IP': '127.0.0.1',
    'CF-Connecting-IP': '127.0.0.1'
}

# Use non-standard ports
# Use HTTP instead of HTTPS
# Use random User-Agents
# Use Tor exit nodes