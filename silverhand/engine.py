"""
SilverHand Engine - Core scanning and analysis engine
Handles all security scanning modules and result processing
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Import PoC generator
try:
    from .poc import PoCGenerator
except ImportError:
    PoCGenerator = None

class SilverHandEngine:
    """Main scanning engine for SilverHand toolkit"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.results = {}
        self.scanners = {}
        self._load_scanners()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('SilverHand')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_scanners(self):
        """Load available scanning modules"""
        try:
            # LFI Scanner
            from .scanner.lfi_scanner import LFIScanner
            self.scanners['lfi'] = LFIScanner()
            
            # SQL Scanner
            from .scanner.sql_scanner import SQLScanner
            self.scanners['sql'] = SQLScanner()
            
            # XSS Scanner
            from .scanner.xss_scanner import XSSScanner
            self.scanners['xss'] = XSSScanner()
            
            # Note: Other scanners would be loaded here
            # For now, we'll simulate their functionality
            
            self.logger.info(f"Loaded {len(self.scanners)} scanning modules")
            
        except ImportError as e:
            self.logger.warning(f"Some scanners not available: {e}")
    
    def run_scan(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run security scan based on configuration"""
        target = config['target']
        modules = config.get('modules', [])
        threads = config.get('threads', 10)
        
        self.logger.info(f"Starting scan of {target} with modules: {modules}")
        
        scan_results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'config': config,
            'findings': {}
        }
        
        # Run scans in parallel
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_module = {}
            
            for module in modules:
                if module in self.scanners:
                    scanner = self.scanners[module]
                    future = executor.submit(self._run_module_scan, scanner, target, config)
                    future_to_module[future] = module
                else:
                    self.logger.warning(f"Scanner module '{module}' not available")
            
            # Collect results
            for future in as_completed(future_to_module):
                module = future_to_module[future]
                try:
                    result = future.result()
                    
                    # Generate PoC if enabled
                    if config.get('generate_poc', False) and PoCGenerator:
                        poc_gen = PoCGenerator()
                        if 'vulnerabilities' in result:
                            for vuln in result['vulnerabilities']:
                                vuln['poc'] = poc_gen.generate_poc(vuln.get('type', 'unknown'), target)
                    
                    scan_results['findings'][module] = result
                    self.logger.info(f"Module '{module}' completed successfully")
                except Exception as e:
                    self.logger.error(f"Module '{module}' failed: {e}")
                    scan_results['findings'][module] = {'error': str(e)}
        
        # AI analysis if enabled
        if config.get('ai_mode', False):
            scan_results['ai_analysis'] = self._ai_analyze_results(scan_results)
        
        self.results = scan_results
        return scan_results
    
    def _run_module_scan(self, scanner, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single scanner module"""
        try:
            return scanner.scan(target, config)
        except Exception as e:
            self.logger.error(f"Scanner {scanner.__class__.__name__} failed: {e}")
            return {'error': str(e), 'vulnerabilities': []}
    
    def _ai_analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze results using AI"""
        try:
            from .ai.analyzer import AIAnalyzer
            analyzer = AIAnalyzer()
            return analyzer.analyze_scan_results(results)
        except ImportError:
            self.logger.warning("AI analyzer not available")
            return {'error': 'AI analyzer not available'}
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return {'error': str(e)}
    
    def display_results(self, results: Dict[str, Any]):
        """Display scan results in console"""
        print("\n" + "="*60)
        print(f"SILVERHAND SCAN RESULTS - {results['target']}")
        print("="*60)
        print(f"Scan Date: {results['timestamp']}")
        print(f"Modules Used: {', '.join(results['findings'].keys())}")
        print("="*60)
        
        total_vulnerabilities = 0
        
        for module, findings in results['findings'].items():
            print(f"\n{module.upper()} SCAN RESULTS:")
            print("-" * 40)
            
            if 'error' in findings:
                print(f"Error: {findings['error']}")
                continue
            
            vulnerabilities = findings.get('vulnerabilities', [])
            total_vulnerabilities += len(vulnerabilities)
            
            if not vulnerabilities:
                print("No vulnerabilities found")
                continue
            
            for i, vuln in enumerate(vulnerabilities, 1):
                severity = vuln.get('severity', 'unknown').upper()
                url = vuln.get('url', 'N/A')
                description = vuln.get('description', 'No description')
                
                print(f"{i}. [{severity}] {url}")
                print(f"   {description}")
                
                if 'recommendation' in vuln:
                    print(f"   Recommendation: {vuln['recommendation']}")
                
                # Display PoC if available
                if 'poc' in vuln and vuln['poc']:
                    print(f"   PoC Generated: ✓")
                    print(f"   PoC Preview: {vuln['poc'][:100]}...")
        
        # AI Analysis
        if 'ai_analysis' in results:
            print(f"\nAI ANALYSIS:")
            print("-" * 40)
            ai_results = results['ai_analysis']
            if 'error' in ai_results:
                print(f"AI Analysis Error: {ai_results['error']}")
            else:
                print(ai_results.get('summary', 'No AI analysis available'))
        
        print(f"\nSUMMARY:")
        print("-" * 40)
        print(f"Total Vulnerabilities Found: {total_vulnerabilities}")
        print("="*60)
    
    def save_results(self, results: Dict[str, Any], filename: str, format_type: str = 'json'):
        """Save results to file in specified format"""
        try:
            if format_type.lower() == 'json':
                self._save_json(results, filename)
            elif format_type.lower() == 'xml':
                self._save_xml(results, filename)
            elif format_type.lower() == 'html':
                self._save_html(results, filename)
            else:
                self._save_txt(results, filename)
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            raise
    
    def _save_json(self, results: Dict[str, Any], filename: str):
        """Save results as JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def _save_xml(self, results: Dict[str, Any], filename: str):
        """Save results as XML"""
        root = ET.Element("silverhand_scan")
        
        # Add metadata
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "target").text = results['target']
        ET.SubElement(metadata, "timestamp").text = results['timestamp']
        
        # Add findings
        findings_elem = ET.SubElement(root, "findings")
        for module, findings in results['findings'].items():
            module_elem = ET.SubElement(findings_elem, "module", name=module)
            
            if 'error' in findings:
                ET.SubElement(module_elem, "error").text = findings['error']
                continue
            
            vulnerabilities = findings.get('vulnerabilities', [])
            for vuln in vulnerabilities:
                vuln_elem = ET.SubElement(module_elem, "vulnerability")
                ET.SubElement(vuln_elem, "severity").text = vuln.get('severity', 'unknown')
                ET.SubElement(vuln_elem, "url").text = vuln.get('url', '')
                ET.SubElement(vuln_elem, "description").text = vuln.get('description', '')
                
                if 'recommendation' in vuln:
                    ET.SubElement(vuln_elem, "recommendation").text = vuln['recommendation']
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
    
    def _save_html(self, results: Dict[str, Any], filename: str):
        """Save results as HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SilverHand Security Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .vulnerability {{ margin: 10px 0; padding: 10px; border-left: 4px solid #e74c3c; background-color: #fdf2f2; }}
        .info {{ margin: 10px 0; padding: 10px; border-left: 4px solid #3498db; background-color: #f2f9fd; }}
        .severity-high {{ border-left-color: #e74c3c; }}
        .severity-medium {{ border-left-color: #f39c12; }}
        .severity-low {{ border-left-color: #f1c40f; }}
        .module {{ margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #34495e; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SilverHand Security Scan Report</h1>
        <p>Target: {results['target']}</p>
        <p>Scan Date: {results['timestamp']}</p>
    </div>
    
    <div class="summary">
        <h2>Scan Summary</h2>
        <p>Modules Used: {', '.join(results['findings'].keys())}</p>
    </div>
"""
        
        for module, findings in results['findings'].items():
            html_content += f"""
    <div class="module">
        <h2>{module.upper()} Scan Results</h2>
"""
            
            if 'error' in findings:
                html_content += f'<div class="info"><p>Error: {findings["error"]}</p></div>'
                continue
            
            vulnerabilities = findings.get('vulnerabilities', [])
            if not vulnerabilities:
                html_content += '<div class="info"><p>No vulnerabilities found</p></div>'
            else:
                for vuln in vulnerabilities:
                    severity = vuln.get('severity', 'unknown')
                    html_content += f"""
        <div class="vulnerability severity-{severity.lower()}">
            <h3>[{severity.upper()}] {vuln.get('url', 'N/A')}</h3>
            <p>{vuln.get('description', 'No description')}</p>
"""
                    if 'recommendation' in vuln:
                        html_content += f'<p><strong>Recommendation:</strong> {vuln["recommendation"]}</p>'
                    html_content += '</div>'
            
            html_content += '</div>'
        
        html_content += """
</body>
</html>
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _save_txt(self, results: Dict[str, Any], filename: str):
        """Save results as plain text"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"SILVERHAND SECURITY SCAN REPORT\n")
            f.write(f"Target: {results['target']}\n")
            f.write(f"Scan Date: {results['timestamp']}\n")
            f.write(f"Modules: {', '.join(results['findings'].keys())}\n")
            f.write("="*60 + "\n\n")
            
            for module, findings in results['findings'].items():
                f.write(f"{module.upper()} SCAN RESULTS:\n")
                f.write("-" * 40 + "\n")
                
                if 'error' in findings:
                    f.write(f"Error: {findings['error']}\n\n")
                    continue
                
                vulnerabilities = findings.get('vulnerabilities', [])
                if not vulnerabilities:
                    f.write("No vulnerabilities found\n\n")
                else:
                    for i, vuln in enumerate(vulnerabilities, 1):
                        severity = vuln.get('severity', 'unknown').upper()
                        f.write(f"{i}. [{severity}] {vuln.get('url', 'N/A')}\n")
                        f.write(f"   {vuln.get('description', 'No description')}\n")
                        
                        if 'recommendation' in vuln:
                            f.write(f"   Recommendation: {vuln['recommendation']}\n")
                        f.write("\n")