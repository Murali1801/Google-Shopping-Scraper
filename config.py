import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Browser Configuration
BROWSER_CONFIG = {
    "build": "Google Images Scraper",
    "name": "Images Results Extraction",
    "platform": "Windows 10",
    "browserName": "Chrome",
    "version": "latest",
    "resolution": "1920x1080",
    "selenium_version": "4.0.0",
    "chrome.driver": "latest",
    "visual": True,
    "video": True,
    "console": True,
    "network": True,
    "headless": False
}

# Google Shopping URLs
GOOGLE_SHOPPING_BASE_URL = "https://www.google.com/search"
GOOGLE_SHOPPING_PARAMS = {
    "tbm": "shop",
    "hl": "en",
    "gl": "in"
}

# Scraping Configuration
MAX_RESULTS_PER_CATEGORY = 5
DELAY_BETWEEN_REQUESTS = 2  # seconds
PAGE_LOAD_TIMEOUT = 30      # seconds
IMPLICIT_WAIT = 10          # seconds 