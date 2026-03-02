# في بداية ملف silver.py أضف
import base64
from pathlib import Path

def load_logo_base64():
    """Load logo as base64 for embedding"""
    logo_path = Path("logos/silver_logo_3d.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def show_logo():
    """Display logo in terminal"""
    ascii_logo_path = Path("logos/silver_ascii_logo.txt")
    if ascii_logo_path.exists():
        with open(ascii_logo_path, "r") as f:
            print(f.read())
    else:
        # Fallback to simple header
        print("""
╔════════════════════════════════════╗
║        SILVER FRAMEWORK v4.0       ║
║      Zero-Day Vulnerability Hunter  ║
║                                    ║
║        Developer: SayerLinux        ║
║    Email: SaudiLinux1@gmail.com     ║
╚════════════════════════════════════╝
        """)