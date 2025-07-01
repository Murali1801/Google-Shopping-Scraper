# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    x11-utils \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxfixes3 \
    libxshmfence1 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libatk1.0-0 \
    libgdk-pixbuf2.0-0 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo-gobject2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libatspi2.0-0 \
    libxss1 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo-gobject2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chrome for Testing and matching ChromeDriver
RUN CHROME_VERSION=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])") && \
    wget -O /tmp/chrome-linux64.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip" && \
    wget -O /tmp/chromedriver-linux64.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chrome-linux64.zip -d /opt/ && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome && \
    ln -s /opt/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /opt/chrome-linux64/chrome /opt/chromedriver-linux64/chromedriver && \
    rm /tmp/chrome-linux64.zip /tmp/chromedriver-linux64.zip

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 scraper \
    && chown -R scraper:scraper /app

# Switch to non-root user
USER scraper

# Expose port for Flask API
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Health check for Flask API
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)" || exit 1

# Default command with Xvfb for virtual display and Flask API
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 & python app.py"] 