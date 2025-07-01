# 🐳 Google Shopping Scraper - Docker Edition

A containerized web scraper that extracts Google Shopping results using Selenium and Chrome in a Docker environment.

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo>
cd "Outfit Rec"

# Make the run script executable
chmod +x run_docker.sh
```

### 2. Run the Scraper
```bash
# Option 1: Use the convenience script
./run_docker.sh

# Option 2: Manual Docker commands
docker-compose build
docker-compose up scraper
```

## 📁 Project Structure

```
Outfit Rec/
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Multi-container setup
├── docker_scraper.py          # Docker-optimized scraper
├── run_docker.sh             # Convenience script
├── requirements.txt           # Python dependencies
├── config.py                 # Configuration settings
├── input.json                # Search queries input
├── .dockerignore             # Files to exclude from build
├── data/                     # Output directory (mounted volume)
└── logs/                     # Logs directory (mounted volume)
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# LambdaTest Credentials (optional for Docker version)
LAMBDATEST_USERNAME=your_lambdatest_username
LAMBDATEST_ACCESS_KEY=your_lambdatest_access_key

# Docker Configuration
PYTHONUNBUFFERED=1
```

### Input Data
The scraper reads search queries from `input.json`:

```json
{
  "data": "{\"top_wear_search_engine_query\": \"vertical striped shirts for men\", ...}",
  "status": "success"
}
```

## 🐳 Docker Features

### Anti-Detection Measures
- **Headless Chrome** with stealth options
- **Random user agents** for each session
- **Human-like delays** and mouse movements
- **Multiple fallback selectors** for element detection
- **Natural search flow** (homepage → search → shopping tab)

### Container Benefits
- **Isolated environment** - No conflicts with local system
- **Consistent setup** - Same environment everywhere
- **Easy scaling** - Run multiple instances
- **Portable** - Works on any Docker host

### Volume Mounts
- `./data:/app/data` - Results are saved here
- `./logs:/app/logs` - Log files are stored here

## 📊 Output

Results are saved to `data/scraped_results.json` in the format:

```json
{
  "top_wear_search_engine_query_result1_url": "https://...",
  "top_wear_search_engine_query_result1_image_url": "https://...",
  "top_wear_search_engine_query_result1_buy_now_url": "https://...",
  ...
}
```

## 🛠️ Advanced Usage

### Custom Docker Build
```bash
# Build with custom tag
docker build -t my-scraper .

# Run with custom name
docker run --name my-scraper-container my-scraper
```

### Docker Compose Services
```bash
# Run only the scraper
docker-compose up scraper

# Run in background
docker-compose up -d scraper

# View logs
docker-compose logs -f scraper

# Stop services
docker-compose down
```

### Development Mode
```bash
# Run with volume mount for live code changes
docker run -v $(pwd):/app -it my-scraper python docker_scraper.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Chrome crashes**
   ```bash
   # Check container logs
   docker-compose logs scraper
   
   # Restart container
   docker-compose restart scraper
   ```

2. **Permission issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER data/ logs/
   ```

3. **Build failures**
   ```bash
   # Clean build
   docker-compose build --no-cache
   ```

### Debug Mode
```bash
# Run with debug output
docker-compose run --rm scraper python -u docker_scraper.py
```

## 📈 Performance Tips

1. **Resource allocation**
   ```yaml
   # In docker-compose.yml
   services:
     scraper:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

2. **Parallel scraping**
   ```bash
   # Run multiple instances
   docker-compose up --scale scraper=3
   ```

3. **Caching**
   ```bash
   # Use Docker layer caching
   docker-compose build --parallel
   ```

## 🔒 Security

- **Non-root user** - Container runs as `scraper` user
- **Read-only filesystem** - Except for data volumes
- **No privileged mode** - Minimal permissions
- **Network isolation** - Custom Docker network

## 📝 Logging

Logs are available in multiple ways:

```bash
# Container logs
docker-compose logs scraper

# File logs (in ./logs directory)
tail -f logs/scraper.log

# Real-time logs
docker-compose logs -f scraper
```

## 🚀 Production Deployment

### Docker Swarm
```bash
# Deploy to swarm
docker stack deploy -c docker-compose.yml scraper-stack
```

### Kubernetes
```yaml
# Example deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scraper
spec:
  replicas: 3
  selector:
    matchLabels:
      app: scraper
  template:
    metadata:
      labels:
        app: scraper
    spec:
      containers:
      - name: scraper
        image: scraper:latest
        volumeMounts:
        - name: data
          mountPath: /app/data
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## 📄 License

This project is for educational purposes only. Please respect website terms of service and robots.txt files.

# 🟢 Deploying to Render

You can deploy this Dockerized Flask API (with Selenium/Chrome) to [Render](https://render.com) for cloud access.

## 1. Push to GitHub
- Commit all code (including Dockerfile, app.py, requirements.txt, etc.) to a GitHub repo.

## 2. Create a Web Service on Render
- Go to https://dashboard.render.com/
- Click **New +** > **Web Service**
- Connect your GitHub repo and select this project.
- **Environment:** Docker
- **Build Command:** *(leave blank)*
- **Start Command:** *(leave blank)*
- **Port:** 5000 (Flask default, already exposed in Dockerfile)
- **Instance Type:** Starter is fine for testing, but Selenium/Chrome may require a Standard or higher plan for production.

## 3. Health Check
- Render will use the `/health` endpoint (already provided by app.py) to check service status.

## 4. Test Your API
- After deploy, your API will be at `https://your-app.onrender.com/scrape`
- Use Postman or `curl` to POST your input JSON.
- Health endpoint: `https://your-app.onrender.com/health`

## 5. Notes
- **Resource Usage:** Headless Chrome is resource-intensive. If you see crashes or timeouts, upgrade your Render instance.
- **Timeouts:** Free/Starter plans have request timeouts (max 15 min). Long scrapes may be cut off.
- **Local Testing:** Always test locally with Docker before deploying. 