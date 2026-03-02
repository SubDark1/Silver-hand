# Intelligent fuzzing:
# - Grammar-based
# - Mutation-based
# - Generation-based
# - Protocol-aware

for payload in generate_payloads(count=10000):
    response = send_payload(payload)
    if detect_crash(response) or detect_info_leak(response):
        analyze_payload(payload)