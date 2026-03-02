# Clone the repository
git clone https://github.com/SayerLinux/silver.git
cd silver

# Run installation script
chmod +x install.sh
./install.sh

# Or install manually
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt