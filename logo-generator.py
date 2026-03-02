#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SILVER Framework - Advanced Logo Generator
Developer: SayerLinux
Email: SaudiLinux1@gmail.com
"""

import os
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import colorsys

class SilverLogoGenerator:
    """Professional Logo Generator for SILVER Framework"""
    
    def __init__(self):
        self.output_dir = "logos"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_3d_glowing_logo(self):
        """Generate 3D Glowing SILVER Logo"""
        # Create high-resolution image
        size = (1024, 1024)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background gradient
        for i in range(size[1]):
            # Dark blue to black gradient
            r = int(10 + (i / size[1]) * 20)
            g = int(20 + (i / size[1]) * 30)
            b = int(50 + (i / size[1]) * 60)
            draw.rectangle([(0, i), (size[0], i+1)], fill=(r, g, b, 255))
        
        # Draw metallic S
        center_x, center_y = size[0]//2, size[1]//2
        
        # Outer glow
        for radius in range(50, 200, 2):
            alpha = max(0, 255 - radius * 2)
            draw.ellipse(
                [(center_x - radius, center_y - radius),
                 (center_x + radius, center_y + radius)],
                outline=(100, 150, 255, alpha),
                width=1
            )
        
        # Main SILVER text with 3D effect
        try:
            # Try to load a bold font
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "C:\\Windows\\Fonts\\Arial.ttf"
            ]
            
            font = None
            for path in font_paths:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, 200)
                    break
            
            if font is None:
                font = ImageFont.load_default()
            
            # Draw 3D layers
            text = "SILVER"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = center_x - text_width // 2
            text_y = center_y - text_height // 2 - 50
            
            # Shadow layers
            for offset in range(10, 0, -1):
                draw.text(
                    (text_x + offset, text_y + offset),
                    text,
                    font=font,
                    fill=(30, 30, 50, 100)
                )
            
            # Main text with gradient
            for i, char in enumerate(text):
                char_x = text_x + i * (text_width // len(text))
                # Silver gradient
                color = (192 + i*10, 192 + i*5, 200 + i*5, 255)
                draw.text((char_x, text_y), char, font=font, fill=color)
            
            # Draw "ZERO-DAY" subtitle
            sub_font = ImageFont.truetype(font_paths[0], 80) if os.path.exists(font_paths[0]) else ImageFont.load_default()
            sub_text = "ZERO-DAY HUNTER"
            sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
            sub_width = sub_bbox[2] - sub_bbox[0]
            draw.text(
                (center_x - sub_width // 2, text_y + text_height + 20),
                sub_text,
                font=sub_font,
                fill=(100, 200, 255, 255)
            )
            
        except Exception as e:
            print(f"Font error: {e}")
            # Fallback to simple shapes
            self._draw_fallback_logo(draw, center_x, center_y)
        
        # Apply glow effect
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        img = ImageEnhance.Brightness(img).enhance(1.2)
        
        # Save
        output_path = os.path.join(self.output_dir, "silver_logo_3d.png")
        img.save(output_path, "PNG")
        print(f"[✓] 3D Logo saved: {output_path}")
        return output_path
    
    def generate_cyberpunk_logo(self):
        """Generate Cyberpunk Style SILVER Logo"""
        size = (1024, 1024)
        img = Image.new('RGBA', size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        
        # Cyberpunk grid background
        grid_color = (0, 255, 255, 30)  # Cyan with low opacity
        
        # Draw vertical lines
        for x in range(0, size[0], 50):
            draw.line([(x, 0), (x, size[1])], fill=grid_color, width=1)
        
        # Draw horizontal lines
        for y in range(0, size[1], 50):
            draw.line([(0, y), (size[0], y)], fill=grid_color, width=1)
        
        # Draw perspective lines
        center_x, center_y = size[0]//2, size[1]//2
        for i in range(0, 360, 45):
            import math
            angle = math.radians(i)
            end_x = center_x + int(math.cos(angle) * 600)
            end_y = center_y + int(math.sin(angle) * 600)
            draw.line([(center_x, center_y), (end_x, end_y)], 
                     fill=(255, 0, 255, 50), width=1)
        
        # Draw main text with neon effect
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 180)
            
            # Neon glow
            text = "SILVER"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = center_x - text_width // 2
            text_y = center_y - 100
            
            # Multiple glow layers
            for radius in range(20, 0, -2):
                glow_color = (255, 0, 255, 50 - radius*2)
                for offset in [(radius, 0), (-radius, 0), (0, radius), (0, -radius)]:
                    draw.text(
                        (text_x + offset[0], text_y + offset[1]),
                        text,
                        font=font,
                        fill=glow_color
                    )
            
            # Main text
            draw.text((text_x, text_y), text, font=font, fill=(0, 255, 255, 255))
            
            # Binary rain effect
            binary_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            for x in range(0, size[0], 40):
                for y in range(0, size[1], 40):
                    if np.random.random() > 0.7:
                        binary = "10"[np.random.randint(0, 2)]
                        draw.text((x, y), binary, font=binary_font, fill=(0, 255, 0, 100))
            
        except Exception as e:
            print(f"Font error in cyberpunk: {e}")
        
        output_path = os.path.join(self.output_dir, "silver_logo_cyberpunk.png")
        img.save(output_path, "PNG")
        print(f"[✓] Cyberpunk Logo saved: {output_path}")
        return output_path
    
    def generate_minimalist_logo(self):
        """Generate Minimalist SILVER Logo"""
        size = (512, 512)
        img = Image.new('RGBA', size, (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = size[0]//2, size[1]//2
        
        # Draw abstract S shape
        points = []
        for i in range(0, 360, 10):
            angle = math.radians(i)
            if i < 180:
                r = 150
            else:
                r = 120
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle) * 0.5
            points.append((x, y))
        
        # Draw the path
        if len(points) > 1:
            for i in range(len(points)-1):
                draw.line([points[i], points[i+1]], fill=(100, 100, 100, 255), width=5)
        
        # Draw small circles at key points
        for i, point in enumerate(points[::10]):
            draw.ellipse(
                [(point[0]-5, point[1]-5), (point[0]+5, point[1]+5)],
                fill=(0, 150, 255, 255),
                outline=None
            )
        
        output_path = os.path.join(self.output_dir, "silver_logo_minimalist.png")
        img.save(output_path, "PNG")
        print(f"[✓] Minimalist Logo saved: {output_path}")
        return output_path
    
    def generate_ascii_logo(self):
        """Generate ASCII Art Logo for terminal"""
        ascii_logo = """
\033[38;5;39m
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║       ███████╗██╗██╗░░░░░██╗░░░██╗███████╗██████╗░               ║
║       ██╔════╝██║██║░░░░░██║░░░██║██╔════╝██╔══██╗               ║
║       ███████╗██║██║░░░░░╚██╗░██╔╝█████╗░░██████╔╝               ║
║       ╚════██║██║██║░░░░░░╚████╔╝░██╔══╝░░██╔══██╗               ║
║       ███████║██║███████╗░░╚██╔╝░░███████╗██║░░██║               ║
║       ╚══════╝╚═╝╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝               ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   ░██████╗███████╗██████╗░░█████╗░  ██████╗░░█████╗░██╗░░░██╗   ║
║   ██╔════╝██╔════╝██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗╚██╗░██╔╝   ║
║   ╚█████╗░█████╗░░██████╔╝██║░░██║  ██║░░██║██║░░██║░╚████╔╝░   ║
║   ░╚═══██╗██╔══╝░░██╔══██╗██║░░██║  ██║░░██║██║░░██║░░╚██╔╝░░   ║
║   ██████╔╝███████╗██║░░██║╚█████╔╝  ██████╔╝╚█████╔╝░░░██║░░░   ║
║   ╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░  ╚═════╝░░╚════╝░░░░╚═╝░░░   ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   \033[38;5;226m▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\033[38;5;39m   ║
║   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ║
║                                                                   ║
║   \033[38;5;46m████████╗███████╗░█████╗░██╗░░██╗███╗░░██╗░█████╗░██╗░░░░░░█████╗░\033[38;5;39m   ║
║   ╚══██╔══╝██╔════╝██╔══██╗██║░░██║████╗░██║██╔══██╗██║░░░░░██╔══██╗   ║
║   ░░░██║░░░█████╗░░██║░░╚═╝███████║██╔██╗██║███████║██║░░░░░██║░░██║   ║
║   ░░░██║░░░██╔══╝░░██║░░██╗██╔══██║██║╚████║██╔══██║██║░░░░░██║░░██║   ║
║   ░░░██║░░░███████╗╚█████╔╝██║░░██║██║░╚███║██║░░██║███████╗╚█████╔╝   ║
║   ░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝░╚════╝░   ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   \033[38;5;208mDeveloper: SayerLinux\033[38;5;39m                                            ║
║   \033[38;5;208mEmail: SaudiLinux1@gmail.com\033[38;5;39m                                       ║
║   \033[38;5;208mVersion: 4.0.0 DARK MIRROR\033[38;5;39m                                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
\033[0m
"""
        
        output_path = os.path.join(self.output_dir, "silver_ascii_logo.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            # Remove ANSI color codes for file
            import re
            clean_logo = re.sub(r'\033\[[0-9;]*m', '', ascii_logo)
            f.write(clean_logo)
        
        print(f"[✓] ASCII Logo saved: {output_path}")
        return ascii_logo
    
    def generate_favicon(self):
        """Generate favicon.ico for web interface"""
        size = (64, 64)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw shield shape
        points = [
            (32, 5),   # Top
            (55, 15),  # Top right
            (55, 35),  # Middle right
            (32, 55),  # Bottom
            (9, 35),   # Middle left
            (9, 15),   # Top left
            (32, 5)    # Back to top
        ]
        
        # Draw shield with gradient
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=(0, 150, 255, 255), width=3)
        
        # Draw "S" inside
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
            draw.text((20, 15), "S", font=font, fill=(255, 255, 255, 255))
        except:
            draw.rectangle([(25, 20), (40, 35)], fill=(255, 255, 255, 255))
        
        # Save as ICO
        output_path = os.path.join(self.output_dir, "favicon.ico")
        img.save(output_path, format='ICO', sizes=[(64, 64)])
        print(f"[✓] Favicon saved: {output_path}")
        
        # Also save as PNG
        png_path = os.path.join(self.output_dir, "favicon.png")
        img.save(png_path, "PNG")
        
        return output_path
    
    def generate_banner(self):
        """Generate HTML banner for reports"""
        html_banner = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 40px; 
            border-radius: 20px; 
            text-align: center; 
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
    
    <div style="font-size: 80px; 
                font-weight: bold; 
                color: white; 
                text-shadow: 3px 3px 0 #4a4a4a, 
                             6px 6px 0 #3a3a3a,
                             9px 9px 10px rgba(0,0,0,0.5);
                letter-spacing: 10px;
                margin-bottom: 20px;">
        SILVER
    </div>
    
    <div style="font-size: 30px; 
                color: rgba(255,255,255,0.9); 
                text-transform: uppercase; 
                letter-spacing: 15px;
                margin-bottom: 20px;
                border-top: 2px solid rgba(255,255,255,0.3);
                border-bottom: 2px solid rgba(255,255,255,0.3);
                padding: 15px 0;">
        ZERO-DAY HUNTER
    </div>
    
    <div style="display: flex; 
                justify-content: center; 
                gap: 30px; 
                color: white; 
                font-size: 16px;
                opacity: 0.8;">
        <div>🔍 Advanced Scanning</div>
        <div>⚡ Zero-Day Detection</div>
        <div>📊 Professional Reports</div>
    </div>
    
    <div style="margin-top: 30px; 
                color: rgba(255,255,255,0.7); 
                font-size: 14px;">
        Developed by SayerLinux | SaudiLinux1@gmail.com
    </div>
</div>
"""
        
        output_path = os.path.join(self.output_dir, "report_banner.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_banner)
        
        print(f"[✓] Report Banner saved: {output_path}")
        return html_banner
    
    def generate_all(self):
        """Generate all logo variants"""
        print("\n" + "="*60)
        print("🖼️  Generating SILVER Framework Logos")
        print("="*60 + "\n")
        
        # Generate all logos
        self.generate_3d_glowing_logo()
        self.generate_cyberpunk_logo()
        self.generate_minimalist_logo()
        ascii_logo = self.generate_ascii_logo()
        self.generate_favicon()
        self.generate_banner()
        
        # Print ASCII logo to console
        print("\n" + "="*60)
        print("📟 ASCII Logo Preview:")
        print("="*60)
        print(ascii_logo)
        
        print("\n" + "="*60)
        print("✅ All logos generated successfully!")
        print(f"📁 Logos saved in: {os.path.abspath(self.output_dir)}")
        print("="*60 + "\n")
        
        # Create index.html preview
        self.create_preview_html()
    
    def create_preview_html(self):
        """Create HTML preview of all logos"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILVER Framework - Logo Preview</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 40px;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 50px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .logo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }
        .logo-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s;
        }
        .logo-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }
        .logo-card img {
            max-width: 100%;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        .logo-card h3 {
            margin: 10px 0;
            font-size: 1.5em;
        }
        .logo-card p {
            margin: 5px 0;
            opacity: 0.8;
        }
        .footer {
            text-align: center;
            padding: 40px;
            background: rgba(0,0,0,0.2);
            border-radius: 20px;
            margin-top: 50px;
        }
        .footer a {
            color: white;
            text-decoration: none;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 5px;
        }
        .footer a:hover {
            border-bottom-color: white;
        }
        .badge {
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 50px;
            display: inline-block;
            margin: 10px 0;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ SILVER Framework Logos</h1>
        
        <div class="logo-grid">
            <div class="logo-card">
                <img src="silver_logo_3d.png" alt="3D Logo">
                <h3>✨ 3D Glowing Logo</h3>
                <p>Professional metallic finish with glow effects</p>
                <span class="badge">Recommended for branding</span>
            </div>
            
            <div class="logo-card">
                <img src="silver_logo_cyberpunk.png" alt="Cyberpunk Logo">
                <h3>⚡ Cyberpunk Edition</h3>
                <p>Neon cyan and magenta with binary rain</p>
                <span class="badge">For dark themes</span>
            </div>
            
            <div class="logo-card">
                <img src="silver_logo_minimalist.png" alt="Minimalist Logo">
                <h3>🎯 Minimalist</h3>
                <p>Clean and modern design</p>
                <span class="badge">For favicons & small displays</span>
            </div>
            
            <div class="logo-card">
                <img src="favicon.png" alt="Favicon">
                <h3>🔷 Favicon</h3>
                <p>64x64 icon for web interface</p>
                <span class="badge">ICO format available</span>
            </div>
        </div>
        
        <div class="footer">
            <h2>👨‍💻 Developer Information</h2>
            <p><strong>Developer:</strong> SayerLinux</p>
            <p><strong>Email:</strong> SaudiLinux1@gmail.com</p>
            <p><strong>Version:</strong> 4.0.0 DARK MIRROR</p>
            <p style="margin-top: 20px;">
                <a href="silver_ascii_logo.txt" target="_blank">📄 View ASCII Logo</a> | 
                <a href="report_banner.html" target="_blank">📊 View Report Banner</a>
            </p>
            <p style="margin-top: 40px; font-size: 0.9em; opacity: 0.6;">
                © 2024 SayerLinux. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        preview_path = os.path.join(self.output_dir, "preview.html")
        with open(preview_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[✓] Preview HTML saved: {preview_path}")

# ===================================================================
# MAIN EXECUTION
# ===================================================================

def main():
    """Generate all logos"""
    print("\033[96m" + "="*60)
    print("  ███████╗██╗██╗░░░░░██╗░░░██╗███████╗██████╗░")
    print("  ██╔════╝██║██║░░░░░██║░░░██║██╔════╝██╔══██╗")
    print("  ███████╗██║██║░░░░░╚██╗░██╔╝█████╗░░██████╔╝")
    print("  ╚════██║██║██║░░░░░░╚████╔╝░██╔══╝░░██╔══██╗")
    print("  ███████║██║███████╗░░╚██╔╝░░███████╗██║░░██║")
    print("  ╚══════╝╚═╝╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝")
    print("="*60)
    print("\033[93mSILVER Framework - Professional Logo Generator\033[0m")
    print("\033[92mDeveloper: SayerLinux\033[0m")
    print("\033[92mEmail: SaudiLinux1@gmail.com\033[0m")
    print("\033[96m" + "="*60 + "\033[0m\n")
    
    # Check for PIL
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("\033[91m[!] Installing required packages...\033[0m")
        os.system("pip install Pillow numpy")
        from PIL import Image, ImageDraw, ImageFont
    
    # Generate logos
    generator = SilverLogoGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main()