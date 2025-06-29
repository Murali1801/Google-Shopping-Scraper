import json
import time
import random
import urllib.parse
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import config

class GoogleShoppingScraper:
    def __init__(self):
        self.driver = None
        self.ua = UserAgent()
        self.results = {}
        
    def setup_driver(self):
        """Setup local Chrome WebDriver with anti-detection measures"""
        try:
            # Chrome options for anti-detection
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Headless mode for Docker
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            
            # Random user agent
            user_agent = self.ua.random
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # Additional anti-detection measures
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # Faster loading
            chrome_options.add_argument("--disable-javascript")  # Disable JS for faster loading
            
            # Use local Chrome binary
            chrome_options.binary_location = "/opt/chrome-linux64/chrome"
            
            # Create driver with local Chrome
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Set timeouts
            self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(config.IMPLICIT_WAIT)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Local Chrome WebDriver setup successful")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup WebDriver: {str(e)}")
            return False
    
    def human_like_delay(self, min_delay=1, max_delay=3):
        """Add human-like random delays"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def scroll_randomly(self):
        """Perform random scrolling to appear more human-like"""
        try:
            scroll_amount = random.randint(300, 800)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            self.human_like_delay(0.5, 1.5)
        except:
            pass
    
    def search_google_shopping(self, query: str) -> bool:
        """Search Google Shopping with the given query"""
        try:
            # Construct Google Shopping URL
            params = config.GOOGLE_SHOPPING_PARAMS.copy()
            params['q'] = query
            
            url = f"{config.GOOGLE_SHOPPING_BASE_URL}?{urllib.parse.urlencode(params)}"
            
            print(f"🔍 Searching: {query}")
            print(f"📄 URL: {url}")
            
            # Navigate to Google Shopping
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-docid]"))
            )
            
            # Human-like behavior
            self.human_like_delay(2, 4)
            self.scroll_randomly()
            
            return True
            
        except TimeoutException:
            print(f"⚠️ Timeout waiting for search results: {query}")
            return False
        except Exception as e:
            print(f"❌ Error searching: {str(e)}")
            return False
    
    def extract_shopping_results(self, category: str) -> List[Dict]:
        """Extract shopping results from the current page"""
        results = []
        
        try:
            # Wait for shopping results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-docid]"))
            )
            
            # Find all shopping result containers
            result_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-docid]")
            
            print(f"📊 Found {len(result_elements)} results for {category}")
            
            for i, element in enumerate(result_elements[:config.MAX_RESULTS_PER_CATEGORY]):
                try:
                    result_data = self.extract_single_result(element, i + 1)
                    if result_data:
                        results.append(result_data)
                        print(f"✅ Extracted result {i + 1} for {category}")
                        
                except Exception as e:
                    print(f"⚠️ Error extracting result {i + 1}: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error extracting results for {category}: {str(e)}")
            
        return results
    
    def extract_single_result(self, element, result_number: int) -> Optional[Dict]:
        """Extract data from a single shopping result element"""
        try:
            result_data = {}
            
            # Extract product URL
            try:
                link_element = element.find_element(By.CSS_SELECTOR, "a[href*='/shopping/product/']")
                result_data['url'] = link_element.get_attribute('href')
            except:
                result_data['url'] = ""
            
            # Extract image URL
            try:
                img_element = element.find_element(By.CSS_SELECTOR, "img")
                result_data['image_url'] = img_element.get_attribute('src')
            except:
                result_data['image_url'] = ""
            
            # Extract buy now URL
            try:
                buy_button = element.find_element(By.CSS_SELECTOR, "a[href*='buy']")
                result_data['buy_now_url'] = buy_button.get_attribute('href')
            except:
                result_data['buy_now_url'] = ""
            
            return result_data
            
        except Exception as e:
            print(f"⚠️ Error extracting single result: {str(e)}")
            return None
    
    def scrape_category(self, category: str, query: str) -> bool:
        """Scrape results for a specific category"""
        try:
            # Search for the category
            if not self.search_google_shopping(query):
                return False
            
            # Extract results
            results = self.extract_shopping_results(category)
            
            if results:
                self.results[category] = results
                print(f"✅ Successfully scraped {len(results)} results for {category}")
                return True
            else:
                print(f"⚠️ No results found for {category}")
                return False
                
        except Exception as e:
            print(f"❌ Error scraping category {category}: {str(e)}")
            return False
    
    def format_output(self) -> Dict:
        """Format the results according to the required output structure"""
        formatted_results = {}
        
        for category, results in self.results.items():
            category_prefix = category.replace('_', '_wear_')
            
            for i, result in enumerate(results, 1):
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_url"] = result.get('url', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_image_url"] = result.get('image_url', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_buy_now_url"] = result.get('buy_now_url', '')
        
        return formatted_results
    
    def run_scraper(self, input_file: str = "input.json") -> Dict:
        """Main method to run the scraper"""
        try:
            # Load input data
            with open(input_file, 'r') as f:
                input_data = json.load(f)
            
            # Parse the nested JSON string
            data = json.loads(input_data['data'])
            
            # Extract search queries
            queries = {
                'top_wear': data['top_wear_search_engine_query'],
                'bottom_wear': data['bottom_wear_search_engine_query'],
                'shoes': data['shoes_search_engine_query'],
                'color_recommendations': data['color_recommendations_search_engine_query']
            }
            
            print("🚀 Starting Google Shopping Scraper with Docker Chrome")
            print(f"📋 Queries to scrape: {list(queries.keys())}")
            
            # Setup driver
            if not self.setup_driver():
                return {"error": "Failed to setup WebDriver"}
            
            # Scrape each category
            for category, query in queries.items():
                print(f"\n🎯 Scraping category: {category}")
                print(f"🔍 Query: {query}")
                
                success = self.scrape_category(category, query)
                
                if success:
                    # Add delay between categories
                    self.human_like_delay(config.DELAY_BETWEEN_REQUESTS, config.DELAY_BETWEEN_REQUESTS + 2)
                else:
                    print(f"⚠️ Failed to scrape {category}")
            
            # Format and return results
            final_results = self.format_output()
            
            print(f"\n✅ Scraping completed! Extracted {len(final_results)} data points")
            return final_results
            
        except Exception as e:
            print(f"❌ Error in main scraper: {str(e)}")
            return {"error": str(e)}
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 WebDriver closed")

def main():
    """Main function to run the scraper"""
    scraper = GoogleShoppingScraper()
    results = scraper.run_scraper()
    
    # Save results to file
    with open('data/scraped_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to 'data/scraped_results.json'")
    print(f"📊 Total results extracted: {len(results)}")
    
    return results

if __name__ == "__main__":
    main() 