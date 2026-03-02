"""
AI Security Assistant Chat Module
Provides interactive AI-powered security analysis and recommendations
"""

import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

class AIChat:
    """AI Security Assistant for interactive security analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or self._load_api_key()
        self.conversation_history = []
        self.session_active = False
        
    def _load_api_key(self) -> Optional[str]:
        """Load API key from environment or config"""
        import os
        return os.getenv('OPENAI_API_KEY') or os.getenv('AI_API_KEY')
    
    def start(self):
        """Start the AI chat session"""
        print("\n" + "="*60)
        print("SILVERHAND AI SECURITY ASSISTANT v3.0")
        print("="*60)
        print("Welcome! I'm your AI security assistant.")
        print("I can help you with:")
        print("• Security vulnerability analysis")
        print("• Exploit development guidance")
        print("• Security best practices")
        print("• Code security review")
        print("• Network security assessment")
        print("\nType 'help' for commands, 'exit' to quit")
        print("="*60)
        
        self.session_active = True
        self._main_loop()
    
    def _main_loop(self):
        """Main chat loop"""
        while self.session_active:
            try:
                user_input = input("\n[AI Assistant] > ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self._end_session()
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'clear':
                    self._clear_history()
                    continue
                
                if user_input.lower() == 'history':
                    self._show_history()
                    continue
                
                # Process user input
                response = self._process_input(user_input)
                print(f"\n[AI]: {response}")
                
                # Add to conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'user': user_input,
                    'ai': response
                })
                
            except KeyboardInterrupt:
                print("\n\nSession interrupted. Type 'exit' to quit.")
            except Exception as e:
                print(f"\n[Error]: {str(e)}")
    
    def _show_help(self):
        """Show available commands"""
        help_text = """
Available Commands:
• help - Show this help message
• clear - Clear conversation history
• history - Show conversation history
• analyze <target> - Analyze a security target
• exploit <vulnerability> - Get exploit guidance
• secure <technology> - Get security hardening tips
• scan <target> - Get scanning recommendations
• • code <language> - Get secure coding practices
• exit - End the session
 
Example queries:
• "Analyze SQL injection vulnerability in PHP"
• "How to exploit XSS in a web application"
• "Secure Apache web server configuration"
• "Best practices for Python web security"
• "How to scan for open ports on a network"
        """
        print(help_text)
    
    def _clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        print("Conversation history cleared.")
    
    def _show_history(self):
        """Show conversation history"""
        if not self.conversation_history:
            print("No conversation history available.")
            return
        
        print("\nConversation History:")
        print("-" * 40)
        for i, entry in enumerate(self.conversation_history[-10:], 1):
            print(f"{i}. User: {entry['user']}")
            print(f"   AI: {entry['ai'][:100]}...")
            print()
    
    def _end_session(self):
        """End the chat session"""
        self.session_active = False
        print("\nThank you for using SilverHand AI Security Assistant!")
        print("Stay secure! 🔒")
    
    def _process_input(self, user_input: str) -> str:
        """Process user input and generate AI response"""
        # Simple rule-based responses for common queries
        user_input_lower = user_input.lower()
        
        # Security analysis patterns
        if any(word in user_input_lower for word in ['analyze', 'analysis', 'vulnerability']):
            return self._generate_security_analysis(user_input)
        
        if any(word in user_input_lower for word in ['exploit', 'exploitation', 'attack']):
            return self._generate_exploit_guidance(user_input)
        
        if any(word in user_input_lower for word in ['secure', 'harden', 'protect']):
            return self._generate_security_tips(user_input)
        
        if any(word in user_input_lower for word in ['scan', 'scanner', 'enumeration']):
            return self._generate_scanning_guidance(user_input)
        
        if any(word in user_input_lower for word in ['code', 'programming', 'development']):
            return self._generate_coding_guidance(user_input)
        
        if any(word in user_input_lower for word in ['network', 'infrastructure']):
            return self._generate_network_security_guidance(user_input)
        
        # Default AI response (simulated)
        return self._generate_default_response(user_input)
    
    def _generate_security_analysis(self, query: str) -> str:
        """Generate security analysis response"""
        responses = [
            "Based on your query, I can help analyze security vulnerabilities. Here's my analysis:\n\n"
            "1. **Vulnerability Assessment**: The issue you've described appears to be a common security flaw.\n"
            "2. **Risk Level**: This could pose a significant risk if exploited by attackers.\n"
            "3. **Impact**: Potential for data breach, unauthorized access, or system compromise.\n"
            "4. **Recommendations**:\n"
            "   • Implement input validation and sanitization\n"
            "   • Use parameterized queries\n"
            "   • Apply principle of least privilege\n"
            "   • Regular security testing and code reviews\n\n"
            "Would you like me to provide specific remediation steps?",
            
            "Security Analysis Complete:\n\n"
            "**Identified Issues**:\n"
            "• Input validation missing\n"
            "• Insufficient access controls\n"
            "• Potential for injection attacks\n\n"
            "**Immediate Actions**:\n"
            "1. Validate all user inputs\n"
            "2. Implement proper authentication\n"
            "3. Use secure coding practices\n"
            "4. Enable security logging\n\n"
            "**Long-term Strategy**: Regular security audits and penetration testing."
        ]
        
        import random
        return random.choice(responses)
    
    def _generate_exploit_guidance(self, query: str) -> str:
        """Generate exploit development guidance"""
        return (
            "I understand you're interested in exploit development for security research.\n\n"
            "**Ethical Considerations**: Always ensure you have proper authorization before testing.\n\n"
            "**General Approach**:\n"
            "1. **Reconnaissance**: Gather information about the target\n"
            "2. **Vulnerability Identification**: Find potential weaknesses\n"
            "3. **Exploit Development**: Create proof-of-concept\n"
            "4. **Testing**: Validate in controlled environment\n"
            "5. **Reporting**: Document findings responsibly\n\n"
            "**Security Research Best Practices**:\n"
            "• Only test on systems you own or have permission to test\n"
            "• Follow responsible disclosure procedures\n"
            "• Document your research methodology\n"
            "• Consider legal and ethical implications\n\n"
            "Would you like guidance on specific vulnerability research techniques?"
        )
    
    def _generate_security_tips(self, query: str) -> str:
        """Generate security hardening tips"""
        return (
            "Here are essential security hardening recommendations:\n\n"
            "**System Hardening**:\n"
            "• Keep all software updated with latest patches\n"
            "• Disable unnecessary services and ports\n"
            "• Implement strong authentication mechanisms\n"
            "• Use encryption for data at rest and in transit\n"
            "• Configure proper logging and monitoring\n\n"
            "**Network Security**:\n"
            "• Deploy firewalls and intrusion detection systems\n"
            "• Segment network properly\n"
            "• Use VPN for remote access\n"
            "• Implement network access controls\n\n"
            "**Application Security**:\n"
            "• Follow secure coding practices\n"
            "• Perform regular security testing\n"
            "• Implement proper input validation\n"
            "• Use security headers\n\n"
            "What specific technology would you like hardening guidance for?"
        )
    
    def _generate_scanning_guidance(self, query: str) -> str:
        """Generate scanning and enumeration guidance"""
        return (
            "Scanning and enumeration are crucial for security assessment. Here's my guidance:\n\n"
            "**Reconnaissance Methodology**:\n"
            "1. **Passive Recon**: Gather information without direct interaction\n"
            "2. **Active Scanning**: Probe target systems directly\n"
            "3. **Service Enumeration**: Identify running services and versions\n"
            "4. **Vulnerability Identification**: Match services to known vulnerabilities\n\n"
            "**Recommended Scanning Approach**:\n"
            "• Start with network mapping (nmap, masscan)\n"
            "• Perform service enumeration on discovered ports\n"
            "• Use vulnerability scanners (OpenVAS, Nessus)\n"
            "• Conduct web application testing (Nikto, Burp Suite)\n"
            "• Test for common misconfigurations\n\n"
            "**Best Practices**:\n"
            "• Always get proper authorization\n"
            "• Document your scanning methodology\n"
            "• Use multiple tools for comprehensive coverage\n"
            "• Validate findings manually\n\n"
            "Need specific scanning techniques for a particular target?"
        )
    
    def _generate_coding_guidance(self, query: str) -> str:
        """Generate secure coding guidance"""
        return (
            "Secure coding is fundamental to application security. Key principles:\n\n"
            "**Input Validation**:\n"
            "• Validate all user inputs on server-side\n"
            "• Use whitelisting approach\n"
            "• Sanitize data before processing\n"
            "• Implement proper error handling\n\n"
            "**Authentication & Authorization**:\n"
            "• Use strong password policies\n"
            "• Implement multi-factor authentication\n"
            "• Apply principle of least privilege\n"
            "• Session management best practices\n\n"
            "**Data Protection**:\n"
            "• Encrypt sensitive data\n"
            "• Use secure communication protocols\n"
            "• Implement proper logging\n"
            "• Protect against injection attacks\n\n"
            "**Code Quality**:\n"
            "• Regular code reviews\n"
            "• Static and dynamic analysis\n"
            "• Security testing integration\n"
            "• Dependency management\n\n"
            "What programming language or framework are you working with?"
        )
    
    def _generate_network_security_guidance(self, query: str) -> str:
        """Generate network security guidance"""
        return (
            "Network security is critical for protecting infrastructure. Here's my guidance:\n\n"
            "**Network Architecture**:\n"
            "• Implement defense in depth strategy\n"
            "• Use network segmentation\n"
            "• Deploy DMZ for public services\n"
            "• Implement proper zoning\n\n"
            "**Access Control**:\n"
            "• Use strong authentication\n"
            "• Implement network access control (NAC)\n"
            "• Configure proper firewall rules\n"
            "• Use VPN for remote access\n\n"
            "**Monitoring & Detection**:\n"
            "• Deploy IDS/IPS systems\n"
            "• Implement SIEM solutions\n"
            "• Enable comprehensive logging\n"
            "• Regular security assessments\n\n"
            "**Incident Response**:\n"
            "• Develop incident response plan\n"
            "• Regular backup and recovery testing\n"
            "• Network traffic analysis\n"
            "• Forensic readiness\n\n"
            "Need specific guidance for your network infrastructure?"
        )
    
    def _generate_default_response(self, query: str) -> str:
        """Generate default AI response"""
        return (
            "I understand you're asking about cybersecurity. As your AI security assistant, I can help with:\n\n"
            "• **Vulnerability Analysis** - Analyze security weaknesses\n"
            "• **Exploit Research** - Guidance on ethical security testing\n"
            "• **Security Hardening** - System and application protection\n"
            "• **Scanning Techniques** - Network and application assessment\n"
            "• **Secure Coding** - Development best practices\n"
            "• **Network Security** - Infrastructure protection\n\n"
            "Please be more specific about what you'd like to know, or type 'help' for available commands.\n\n"
            "Remember: Always ensure you have proper authorization for any security testing activities."
        )
    
    def analyze_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a security finding with AI"""
        try:
            # Simulate AI analysis
            analysis = {
                'risk_level': self._assess_risk_level(finding),
                'exploitability': self._assess_exploitability(finding),
                'impact': self._assess_impact(finding),
                'recommendations': self._generate_recommendations(finding),
                'ai_summary': self._generate_finding_summary(finding)
            }
            return analysis
        except Exception as e:
            return {'error': str(e)}
    
    def _assess_risk_level(self, finding: Dict[str, Any]) -> str:
        """Assess risk level of a finding"""
        severity = finding.get('severity', 'medium').lower()
        if severity in ['critical', 'high']:
            return 'High Risk'
        elif severity == 'medium':
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    def _assess_exploitability(self, finding: Dict[str, Any]) -> str:
        """Assess exploitability of a finding"""
        vuln_type = finding.get('type', '').lower()
        if 'sql' in vuln_type or 'injection' in vuln_type:
            return 'Easily Exploitable'
        elif 'xss' in vuln_type:
            return 'Moderately Exploitable'
        else:
            return 'Requires Expertise'
    
    def _assess_impact(self, finding: Dict[str, Any]) -> str:
        """Assess potential impact of a finding"""
        severity = finding.get('severity', 'medium').lower()
        if severity in ['critical', 'high']:
            return 'System Compromise'
        elif severity == 'medium':
            return 'Data Exposure'
        else:
            return 'Information Disclosure'
    
    def _generate_recommendations(self, finding: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for a finding"""
        vuln_type = finding.get('type', '').lower()
        recommendations = []
        
        if 'sql' in vuln_type:
            recommendations.extend([
                'Use parameterized queries',
                'Implement input validation',
                'Apply least privilege to database users',
                'Enable SQL query logging'
            ])
        elif 'xss' in vuln_type:
            recommendations.extend([
                'Implement output encoding',
                'Use Content Security Policy (CSP)',
                'Validate and sanitize user input',
                'Use secure frameworks'
            ])
        else:
            recommendations.extend([
                'Implement proper input validation',
                'Use security frameworks',
                'Regular security testing',
                'Code review process'
            ])
        
        return recommendations
    
    def _generate_finding_summary(self, finding: Dict[str, Any]) -> str:
        """Generate AI summary of a finding"""
        return (
            f"This {finding.get('type', 'vulnerability')} represents a significant security risk. "
            f"The vulnerability could allow attackers to {finding.get('impact', 'compromise the system')}. "
            f"Immediate remediation is recommended to prevent potential exploitation."
        )