#!/usr/bin/env python3
"""
SilverHand v3.0.0 - Advanced Cybersecurity Toolkit
Main CLI interface for the SilverHand penetration testing framework.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, List

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from silverhand.engine import SilverHandEngine
from silverhand import __version__

class SilverHandCLI:
    """Main CLI interface for SilverHand toolkit"""
    
    def __init__(self):
        self.engine = SilverHandEngine()
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser"""
        parser = argparse.ArgumentParser(
            description=f"SilverHand v{__version__} - Advanced Cybersecurity Toolkit",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  silverhand --target example.com --scan-all
  silverhand --target 192.168.1.1 --port-scan --ports 1-1000
  silverhand --target example.com --xss-scan --ai-mode
  silverhand --list-modules
  silverhand --update
            """
        )
        
        # Main options
        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
        parser.add_argument('--target', '-t', help='Target URL, IP, or domain')
        parser.add_argument('--output', '-o', help='Output file for results')
        parser.add_argument('--format', choices=['json', 'xml', 'txt', 'html'], default='txt',
                          help='Output format (default: txt)')
        
        # Scanning modules
        scan_group = parser.add_argument_group('Scanning Modules')
        scan_group.add_argument('--scan-all', action='store_true', help='Run all available scans')
        scan_group.add_argument('--port-scan', action='store_true', help='Perform port scanning')
        scan_group.add_argument('--ports', help='Port range (e.g., 1-1000 or 80,443,8080)')
        scan_group.add_argument('--xss-scan', action='store_true', help='Scan for XSS vulnerabilities')
        scan_group.add_argument('--sql-scan', action='store_true', help='Scan for SQL injection vulnerabilities')
        scan_group.add_argument('--lfi-scan', action='store_true', help='Scan for Local File Inclusion')
        scan_group.add_argument('--rfi-scan', action='store_true', help='Scan for Remote File Inclusion')
        scan_group.add_argument('--dir-scan', action='store_true', help='Directory and file enumeration')
        scan_group.add_argument('--subdomain-scan', action='store_true', help='Subdomain enumeration')
        
        # AI Features
        ai_group = parser.add_argument_group('AI Features')
        ai_group.add_argument('--ai-mode', action='store_true', help='Enable AI-powered scanning')
        ai_group.add_argument('--ai-chat', action='store_true', help='Start AI security assistant chat')
        ai_group.add_argument('--ai-analyze', help='Analyze security findings with AI')
        
        # Advanced options
        advanced_group = parser.add_argument_group('Advanced Options')
        advanced_group.add_argument('--threads', '-T', type=int, default=10, help='Number of threads (default: 10)')
        advanced_group.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds (default: 30)')
        advanced_group.add_argument('--user-agent', help='Custom User-Agent string')
        advanced_group.add_argument('--proxy', help='Proxy URL (http://host:port)')
        advanced_group.add_argument('--cookies', help='Cookies to include in requests')
        advanced_group.add_argument('--headers', action='append', help='Custom headers (Key: Value)')
        advanced_group.add_argument('--dangerous', action='store_true', help='Enable dangerous tests (use with caution)')
        advanced_group.add_argument('--poc', action='store_true', help='Generate Proof-of-Concept for found vulnerabilities')
        
        # Utility options
        util_group = parser.add_argument_group('Utility Options')
        util_group.add_argument('--list-modules', action='store_true', help='List all available modules')
        util_group.add_argument('--update', action='store_true', help='Update SilverHand to latest version')
        util_group.add_argument('--config', help='Path to configuration file')
        util_group.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
        util_group.add_argument('--quiet', '-q', action='store_true', help='Suppress output except errors')
        
        return parser
    
    def _validate_args(self, args: argparse.Namespace) -> bool:
        """Validate command line arguments"""
        if not any([args.target, args.list_modules, args.update, args.ai_chat]):
            print("Error: No action specified. Use --target, --list-modules, --update, or --ai-chat")
            return False
        
        if args.target and not self._is_valid_target(args.target):
            print(f"Error: Invalid target format: {args.target}")
            return False
        
        if args.ports and not self._is_valid_port_range(args.ports):
            print(f"Error: Invalid port range: {args.ports}")
            return False
        
        return True
    
    def _is_valid_target(self, target: str) -> bool:
        """Validate target format"""
        # Simple validation for IP, domain, or URL
        if target.startswith(('http://', 'https://')):
            return True
        
        # IP validation
        parts = target.split('.')
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            return True
        
        # Domain validation
        if '.' in target and len(target.split('.')) >= 2:
            return True
        
        return False
    
    def _is_valid_port_range(self, ports: str) -> bool:
        """Validate port range format"""
        try:
            if '-' in ports:
                start, end = map(int, ports.split('-'))
                return 1 <= start <= end <= 65535
            elif ',' in ports:
                port_list = [int(p.strip()) for p in ports.split(',')]
                return all(1 <= p <= 65535 for p in port_list)
            else:
                port = int(ports)
                return 1 <= port <= 65535
        except ValueError:
            return False
    
    def _build_scan_config(self, args: argparse.Namespace) -> dict:
        """Build scan configuration from arguments"""
        config = {
            'target': args.target,
            'threads': args.threads,
            'timeout': args.timeout,
            'user_agent': args.user_agent or f'SilverHand/{__version__}',
            'proxy': args.proxy,
            'cookies': args.cookies,
            'headers': self._parse_headers(args.headers) if args.headers else {},
            'ai_mode': args.ai_mode,
            'verbose': args.verbose,
            'quiet': args.quiet,
            'output_file': args.output,
            'output_format': args.format,
            'dangerous': args.dangerous,
            'generate_poc': args.poc
        }
        
        # Add specific scan modules
        if args.scan_all:
            config['modules'] = ['port', 'xss', 'sql', 'lfi', 'rfi', 'dir', 'subdomain']
        else:
            modules = []
            if args.port_scan: modules.append('port')
            if args.xss_scan: modules.append('xss')
            if args.sql_scan: modules.append('sql')
            if args.lfi_scan: modules.append('lfi')
            if args.rfi_scan: modules.append('rfi')
            if args.dir_scan: modules.append('dir')
            if args.subdomain_scan: modules.append('subdomain')
            config['modules'] = modules
        
        # Add port configuration
        if args.ports:
            config['port_range'] = args.ports
        
        return config
    
    def _parse_headers(self, headers: List[str]) -> dict:
        """Parse custom headers"""
        header_dict = {}
        for header in headers:
            if ':' in header:
                key, value = header.split(':', 1)
                header_dict[key.strip()] = value.strip()
        return header_dict
    
    def _list_modules(self):
        """List all available modules"""
        print("Available SilverHand Modules:")
        print("=" * 40)
        
        modules = {
            "Port Scanner": "Scan for open ports and services",
            "XSS Scanner": "Detect Cross-Site Scripting vulnerabilities",
            "SQL Scanner": "Detect SQL injection vulnerabilities", 
            "LFI Scanner": "Detect Local File Inclusion vulnerabilities",
            "RFI Scanner": "Detect Remote File Inclusion vulnerabilities",
            "Directory Scanner": "Enumerate directories and files",
            "Subdomain Scanner": "Enumerate subdomains",
            "AI Security Assistant": "AI-powered security analysis and recommendations"
        }
        
        for module, description in modules.items():
            print(f"• {module:<20} - {description}")
        
        print("\nUse --help for more options and examples")
    
    def _update_silverhand(self):
        """Update SilverHand to latest version"""
        print("Updating SilverHand...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'silverhand'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("SilverHand updated successfully!")
            else:
                print(f"Update failed: {result.stderr}")
        except Exception as e:
            print(f"Update error: {e}")
    
    def _start_ai_chat(self):
        """Start AI security assistant chat"""
        try:
            from silverhand.ai.chat import AIChat
            chat = AIChat()
            chat.start()
        except ImportError:
            print("AI chat module not available. Please install required dependencies.")
    
    def run(self):
        """Main CLI entry point"""
        args = self.parser.parse_args()
        
        # Validate arguments
        if not self._validate_args(args):
            return 1
        
        # Handle utility commands
        if args.list_modules:
            self._list_modules()
            return 0
        
        if args.update:
            self._update_silverhand()
            return 0
        
        if args.ai_chat:
            self._start_ai_chat()
            return 0
        
        # Build configuration and run scans
        try:
            config = self._build_scan_config(args)
            results = self.engine.run_scan(config)
            
            # Handle output
            if args.output:
                self.engine.save_results(results, args.output, args.format)
                print(f"Results saved to {args.output}")
            else:
                self.engine.display_results(results)
            
            return 0
            
        except KeyboardInterrupt:
            print("\nScan interrupted by user")
            return 130
        except Exception as e:
            print(f"Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1

def main():
    """Entry point for console scripts"""
    cli = SilverHandCLI()
    sys.exit(cli.run())

if __name__ == '__main__':
    main()