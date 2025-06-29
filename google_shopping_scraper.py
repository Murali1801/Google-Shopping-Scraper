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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import config
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-client-side-phishing-detection")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-translate")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--disable-component-extensions-with-background-pages")
            chrome_options.add_argument("--disable-extensions-file-access-check")
            chrome_options.add_argument("--disable-extensions-http-throttling")
            chrome_options.add_argument("--disable-hang-monitor")
            chrome_options.add_argument("--disable-prompt-on-repost")
            chrome_options.add_argument("--disable-domain-reliability")
            chrome_options.add_argument("--disable-component-update")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-features=BlinkGenPropertyTrees")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            # Random user agent
            user_agent = self.ua.random
            chrome_options.add_argument(f'--user-agent={user_agent}')
            # Use local ChromeDriver
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(config.IMPLICIT_WAIT)
            # Remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            self.driver.execute_script("Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})")
            print("✅ Local Chrome WebDriver setup successful")
            return True
        except Exception as e:
            print(f"❌ Failed to setup WebDriver: {str(e)}")
            return False
    
    def human_like_delay(self, min_delay=2, max_delay=5):
        """Add human-like random delays"""
        delay = random.uniform(min_delay, max_delay)
        print(f"⏱️ Waiting {delay:.1f} seconds...")
        time.sleep(delay)
    
    def random_mouse_movement(self):
        """Simulate random mouse movements"""
        try:
            actions = ActionChains(self.driver)
            # Random mouse movements
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.1, 0.3))
            actions.perform()
        except:
            pass
    
    def scroll_randomly(self):
        """Perform random scrolling to appear more human-like"""
        try:
            # Multiple scroll actions with pauses
            for _ in range(random.randint(3, 7)):
                scroll_amount = random.randint(200, 600)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 1.5))
                
                # Sometimes scroll back up a bit
                if random.random() < 0.3:
                    self.driver.execute_script(f"window.scrollBy(0, -{random.randint(50, 150)});")
                    time.sleep(random.uniform(0.3, 0.8))
        except:
            pass
    
    def simulate_typing(self, element, text):
        """Simulate human-like typing with random delays"""
        try:
            element.clear()
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
        except:
            element.send_keys(text)
    
    def search_google_shopping(self, query: str) -> bool:
        """Search Google Shopping with the given query"""
        try:
            # First, go to Google homepage
            print("🏠 Going to Google homepage...")
            self.driver.get("https://www.google.com")
            self.human_like_delay(3, 6)
            
            # Simulate human behavior on homepage
            self.random_mouse_movement()
            self.scroll_randomly()
            
            # Find search box and type query
            try:
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )
                
                print(f"⌨️ Typing query: {query}")
                self.simulate_typing(search_box, query)
                self.human_like_delay(1, 2)
                
                # Press Enter
                search_box.send_keys(Keys.RETURN)
                self.human_like_delay(2, 4)
                
                # Click on Shopping tab
                try:
                    shopping_tab = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Shopping') or contains(@aria-label, 'Shopping')]"))
                    )
                    print("🛍️ Clicking Shopping tab...")
                    shopping_tab.click()
                    self.human_like_delay(3, 6)
                except:
                    print("⚠️ Could not find Shopping tab, trying direct URL...")
                    # Fallback to direct URL
                    params = config.GOOGLE_SHOPPING_PARAMS.copy()
                    params['q'] = query
                    url = f"{config.GOOGLE_SHOPPING_BASE_URL}?{urllib.parse.urlencode(params)}"
                    self.driver.get(url)
                    self.human_like_delay(3, 6)
                
            except:
                # Fallback to direct URL
                print("⚠️ Could not find search box, using direct URL...")
                params = config.GOOGLE_SHOPPING_PARAMS.copy()
                params['q'] = query
                url = f"{config.GOOGLE_SHOPPING_BASE_URL}?{urllib.parse.urlencode(params)}"
                self.driver.get(url)
                self.human_like_delay(3, 6)
            
            # Wait for page to load and simulate human behavior
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-docid], .sh-dlr__product-result"))
                )
            except:
                print("⚠️ Could not find shopping results, continuing anyway...")
            
            # More human-like behavior
            self.human_like_delay(2, 4)
            self.random_mouse_movement()
            self.scroll_randomly()
            
            return True
            
        except TimeoutException:
            print(f"⚠️ Timeout waiting for search results: {query}")
            return False
        except Exception as e:
            print(f"❌ Error searching: {str(e)}")
            return False
    
    def extract_external_page_results(self, category: str) -> List[Dict]:
        """Click each product, open external site, extract product info, and return."""
        results = []
        try:
            grid_selector = "div[data-docid], .sh-dgr__content, .sh-dgr__grid-result"
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, grid_selector))
            )
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, grid_selector)
            print(f"📊 Found {len(product_cards)} product cards for {category}")
            max_products = min(len(product_cards), getattr(config, 'MAX_RESULTS_PER_CATEGORY', 10))
            for i, card in enumerate(product_cards[:max_products]):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                    time.sleep(random.uniform(0.5, 1.0))
                    card.click()
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog'], .sh-osd__details"))
                    )
                    sidebar = self.driver.find_element(By.CSS_SELECTOR, "[role='dialog'], .sh-osd__details")
                    # Find and click 'Visit site'
                    try:
                        visit_btn = sidebar.find_element(By.XPATH, ".//a[contains(text(), 'Visit site') or contains(@aria-label, 'Visit site')]")
                        visit_url = visit_btn.get_attribute('href')
                        visit_btn.click()
                        time.sleep(random.uniform(2, 3))
                        # Switch to new tab
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(random.uniform(2, 3))
                        # Extract from external page
                        data = {'external_url': self.driver.current_url}
                        # Title
                        try:
                            data['title'] = self.driver.title
                        except:
                            data['title'] = ''
                        # Price (try common selectors)
                        price = ''
                        try:
                            price_els = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'price') or contains(@id, 'price') or contains(text(), '$')]")
                            for el in price_els:
                                txt = el.text.strip()
                                if '$' in txt and len(txt) < 30:
                                    price = txt
                                    break
                        except:
                            pass
                        data['price'] = price
                        # Image (try og:image, then first <img>)
                        img_url = ''
                        try:
                            og_img = self.driver.find_element(By.XPATH, "//meta[@property='og:image']")
                            img_url = og_img.get_attribute('content')
                        except:
                            try:
                                img = self.driver.find_element(By.TAG_NAME, 'img')
                                img_url = img.get_attribute('src')
                            except:
                                pass
                        data['image_url'] = img_url
                        results.append(data)
                        print(f"✅ Extracted external page result {i+1} for {category}")
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    except Exception as e:
                        print(f"⚠️ Could not extract external page for product {i+1}: {str(e)}")
                        # Try to close tab if open
                        if len(self.driver.window_handles) > 1:
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                    # Close sidebar (click X or send ESC)
                    try:
                        close_btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close'], .sh-osd__close-button")
                        close_btn.click()
                    except:
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    time.sleep(random.uniform(0.8, 1.5))
                except Exception as e:
                    print(f"⚠️ Error extracting product {i+1}: {str(e)}")
                    continue
        except Exception as e:
            print(f"❌ Error extracting external page results for {category}: {str(e)}")
        return results

    def extract_shopping_results(self, category: str) -> List[Dict]:
        """Extract shopping results from the external merchant page for each product."""
        return self.extract_external_page_results(category)
    
    def scrape_category(self, category: str, query: str) -> bool:
        """Scrape results for a specific category"""
        try:
            print(f"\n🎯 Starting to scrape category: {category}")
            print(f"🔍 Query: {query}")
            
            # Search for the category
            if not self.search_google_shopping(query):
                return False
            
            # Additional delay before extraction
            print("⏳ Waiting before extraction...")
            self.human_like_delay(3, 6)
            
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
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_title"] = result.get('title', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_price"] = result.get('price', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_image_url"] = result.get('image_url', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_external_url"] = result.get('external_url', '')
        return formatted_results
    
    def extract_from_google_images(self, query: str, max_images: int = 5) -> list:
        """Search Google Images, click each image, visit site, extract info, and return."""
        results = []
        try:
            # Go to Google homepage
            self.driver.get("https://www.google.com")
            self.human_like_delay(2, 4)
            # Find search box and type query
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            self.simulate_typing(search_box, query)
            self.human_like_delay(1, 2)
            search_box.send_keys(Keys.RETURN)
            self.human_like_delay(2, 4)
            # Click Images tab
            images_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Images') or contains(@aria-label, 'Images')]"))
            )
            images_tab.click()
            self.human_like_delay(2, 4)
            # Find all image results
            image_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.isv-r.PNCib.MSM1fd.BUooTd"))
            )
            print(f"📸 Found {len(image_cards)} image results for query: {query}")
            for i, card in enumerate(image_cards[:max_images]):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                    time.sleep(random.uniform(0.5, 1.0))
                    card.click()
                    # Wait for sidebar/dialog to appear
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog'], .tvh9oe.BIB1wf"))
                    )
                    sidebar = self.driver.find_element(By.CSS_SELECTOR, "[role='dialog'], .tvh9oe.BIB1wf")
                    # Find and click 'Visit site'
                    try:
                        visit_btn = sidebar.find_element(By.XPATH, ".//a[contains(text(), 'Visit') or contains(@aria-label, 'Visit')]")
                        visit_btn.click()
                        time.sleep(random.uniform(2, 3))
                        # Switch to new tab
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(random.uniform(2, 3))
                        # Extract from external page
                        data = {'external_url': self.driver.current_url}
                        # Title
                        try:
                            data['title'] = self.driver.title
                        except:
                            data['title'] = ''
                        # Price (try common selectors)
                        price = ''
                        try:
                            price_els = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'price') or contains(@id, 'price') or contains(text(), '₹') or contains(text(), '$')]")
                            for el in price_els:
                                txt = el.text.strip()
                                if ('₹' in txt or '$' in txt) and len(txt) < 30:
                                    price = txt
                                    break
                        except:
                            pass
                        data['price'] = price
                        # Image (try og:image, then first <img>)
                        img_url = ''
                        try:
                            og_img = self.driver.find_element(By.XPATH, "//meta[@property='og:image']")
                            img_url = og_img.get_attribute('content')
                        except:
                            try:
                                img = self.driver.find_element(By.TAG_NAME, 'img')
                                img_url = img.get_attribute('src')
                            except:
                                pass
                        data['image_url'] = img_url
                        results.append(data)
                        print(f"✅ Extracted external page result {i+1} for query: {query}")
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    except Exception as e:
                        print(f"⚠️ Could not extract external page for image {i+1}: {str(e)}")
                        # Try to close tab if open
                        if len(self.driver.window_handles) > 1:
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                    # Close sidebar (click X or send ESC)
                    try:
                        close_btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close'], .tvh9oe .T3FoJb")
                        close_btn.click()
                    except:
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    time.sleep(random.uniform(0.8, 1.5))
                except Exception as e:
                    print(f"⚠️ Error extracting image {i+1}: {str(e)}")
                    continue
        except Exception as e:
            print(f"❌ Error extracting from Google Images for query '{query}': {str(e)}")
        return results

    def run_scraper(self, input_file: str = "input.json") -> dict:
        """Main method to run the Google Images workflow"""
        try:
            # Load input data
            with open(input_file, 'r') as f:
                input_data = json.load(f)
            data = json.loads(input_data['data'])
            query = data['top_wear_search_engine_query']
            print("🚀 Starting Google Images Scraper")
            if not self.setup_driver():
                return {"error": "Failed to setup WebDriver"}
            self.human_like_delay(5, 8)
            results = self.extract_from_google_images(query, max_images=5)
            print(f"\n✅ Scraping completed! Extracted {len(results)} data points")
            return {"results": results}
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
    with open('scraped_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to 'scraped_results.json'")
    print(f"📊 Total results extracted: {len(results['results'])}")
    
    return results

if __name__ == "__main__":
    main() 