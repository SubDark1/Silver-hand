# Build Docker image
docker build -t silver .

# Run container
docker run -it silver -t https://target.com