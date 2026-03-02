# Fork the repository
git clone https://github.com/YOUR_USERNAME/silver.git
cd silver

# Create development branch
git checkout -b feature/your-feature

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Submit pull request