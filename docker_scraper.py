import json
import time
import random
import urllib.parse
from typing import Dict, List, Optional
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import config
import traceback
import shutil
import os
import re

class GoogleShoppingScraper:
    def __init__(self):
        self.driver = None
        self.ua = UserAgent()
        self.results = {}
        
    def setup_driver(self):
        """Setup undetected Chrome WebDriver with advanced anti-detection measures"""
        try:
            # Copy ChromeDriver to a writable location
            shutil.copy("/usr/bin/chromedriver", "/tmp/chromedriver")
            os.chmod("/tmp/chromedriver", 0o755)
            
            # Chrome options for anti-detection
            chrome_options = uc.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
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
            
            # Set Chrome binary location explicitly for Docker
            chrome_options.binary_location = "/opt/chrome-linux64/chrome"
            
            # Create driver with undetected-chromedriver
            self.driver = uc.Chrome(
                driver_executable_path="/tmp/chromedriver",
                options=chrome_options,
                version_main=None  # Auto-detect Chrome version
            )
            
            # Set timeouts
            self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(config.IMPLICIT_WAIT)
            
            print("✅ Undetected Chrome WebDriver setup successful")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup WebDriver: {str(e)}")
            traceback.print_exc()
            return False
    
    def human_like_delay(self, min_delay=3, max_delay=8):
        """Add human-like random delays"""
        delay = random.uniform(min_delay, max_delay)
        print(f"⏱️ Waiting {delay:.1f} seconds...")
        time.sleep(delay)
    
    def random_mouse_movement(self):
        """Simulate random mouse movements"""
        try:
            actions = ActionChains(self.driver)
            # Random mouse movements
            for _ in range(random.randint(3, 7)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.1, 0.5))
            actions.perform()
            print("🖱️ Random mouse movements performed")
        except:
            pass
    
    def scroll_randomly(self):
        """Perform random scrolling to appear more human-like"""
        try:
            # Multiple scroll actions with pauses
            for _ in range(random.randint(3, 7)):
                scroll_amount = random.randint(200, 600)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 2.0))
                
                # Sometimes scroll back up a bit
                if random.random() < 0.3:
                    self.driver.execute_script(f"window.scrollBy(0, -{random.randint(50, 150)});")
                    time.sleep(random.uniform(0.3, 1.0))
            print("📜 Random scrolling performed")
        except:
            pass
    
    def simulate_typing(self, element, text):
        """Simulate human-like typing with random delays"""
        try:
            element.clear()
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))
            print(f"⌨️ Typed: {text}")
        except:
            element.send_keys(text)
    
    def search_google_shopping(self, query: str, first_query: bool = False) -> bool:
        """Search Google Shopping: use direct URL for first query, search bar for subsequent queries."""
        try:
            if first_query:
                print("🌐 Navigating directly to Google Shopping page...")
                params = config.GOOGLE_SHOPPING_PARAMS.copy()
                params['q'] = query
                url = f"{config.GOOGLE_SHOPPING_BASE_URL}?{urllib.parse.urlencode(params)}"
                self.driver.get(url)
                self.human_like_delay(5, 10)
            else:
                print(f"🔄 Typing new query in search bar: {query}")
                try:
                    # Use the <textarea.gLFyf> as the search bar after the first query
                    search_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.gLFyf'))
                    )
                    search_box.clear()
                    self.simulate_typing(search_box, query)
                    self.human_like_delay(1, 2)
                    search_box.send_keys(Keys.RETURN)
                    self.human_like_delay(3, 6)
                except Exception as e:
                    print(f"⚠️ Could not find or use search bar for new query: {e}")
                    return False

            print(f"📄 Page title: {self.driver.title}")
            print(f"📄 Current URL: {self.driver.current_url}")

            if "sorry" in self.driver.current_url.lower() or "captcha" in self.driver.current_url.lower():
                print("⚠️ Detected CAPTCHA or error page")
                return False

            # Wait for any known product card selector
            card_selectors = [
                "li.YBo8bb",
                "div[data-merchant-id]",
                "div[data-docid]",
                ".sh-dlr__product-result",
                "[data-docid]",
                ".sh-dgr__content",
                "div[jscontroller]"
            ]
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.any_of(*[EC.presence_of_element_located((By.CSS_SELECTOR, sel)) for sel in card_selectors])
                )
            except Exception as e:
                print(f"⚠️ Could not find shopping results, continuing anyway... {e}")
                try:
                    print("📄 Page source preview:")
                    page_source = self.driver.page_source[:1000]
                    print(page_source)
                except:
                    pass

            self.human_like_delay(3, 6)
            self.random_mouse_movement()
            self.scroll_randomly()

            return True

        except TimeoutException:
            print(f"⚠️ Timeout waiting for search results: {query}")
            try:
                print("📄 Page source preview:")
                page_source = self.driver.page_source[:1000]
                print(page_source)
            except:
                pass
            return False
        except Exception as e:
            print(f"❌ Error searching: {str(e)}")
            traceback.print_exc()
            return False
    
    def extract_product_page_info(self, driver, original_url):
        """Extract product information from the actual product page"""
        data = {
            "title": "",
            "image_url": "",
            "buy_link": original_url,  # Use the original URL as buy link
            "price": "",
            "url": original_url
        }
        
        try:
            # Wait for page to load
            time.sleep(3)
            
            # Extract title - try multiple selectors for different sites
            title_selectors = [
                'h1',
                '[data-testid="product-title"]',
                '.product-title',
                '.product-name',
                'h1[class*="title"]',
                'h1[class*="name"]',
                '.product-details h1',
                '.product-info h1'
            ]
            
            for selector in title_selectors:
                try:
                    title_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    data["title"] = title_elem.text.strip()
                    if data["title"]:
                        print(f"✅ Found title: {data['title'][:50]}...")
                        break
                except:
                    continue
            
            # Extract image URL - try multiple selectors
            image_selectors = [
                'img[src*="product"]',
                'img[alt*="product"]',
                '.product-image img',
                '.product-img img',
                '.product-gallery img',
                'img[class*="product"]',
                'img[class*="main"]',
                'img[class*="primary"]'
            ]
            
            for selector in image_selectors:
                try:
                    img_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    src = img_elem.get_attribute('src')
                    if src and (src.startswith('http') or src.startswith('//')):
                        if src.startswith('//'):
                            src = 'https:' + src
                        data["image_url"] = src
                        print(f"✅ Found image: {data['image_url'][:50]}...")
                        break
                except:
                    continue
            
            # Extract price - try multiple selectors
            price_selectors = [
                '[data-testid="price"]',
                '.price',
                '.product-price',
                '.current-price',
                '.selling-price',
                'span[class*="price"]',
                'div[class*="price"]',
                '.product-details .price',
                '.product-info .price'
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    # Clean price text (remove extra spaces, currency symbols, etc.)
                    if price_text and any(char.isdigit() for char in price_text):
                        data["price"] = price_text
                        print(f"✅ Found price: {data['price']}")
                        break
                except:
                    continue
            
            print(f"✅ Extracted from product page: Title='{data['title'][:50]}...', Image='{data['image_url'][:50]}...', Price='{data['price']}'")
            
        except Exception as e:
            print(f"⚠️ Error extracting from product page: {str(e)}")
        
        return data

    def _extract_first(self, parent, selectors, attr=None, text=True, field_name=None):
        """Try selectors in order, return first non-empty result. Log each attempt."""
        for selector in selectors:
            try:
                elem = parent.find_element(By.CSS_SELECTOR, selector)
                if attr:
                    value = elem.get_attribute(attr)
                elif text:
                    value = elem.text.strip()
                else:
                    value = elem.get_attribute('outerHTML')
                if value:
                    print(f"[Extract] {field_name or ''} found: '{value}' (selector: {selector})")
                    return value
            except Exception as e:
                print(f"[Extract] {field_name or ''} not found with selector {selector}: {e}")
        print(f"[Extract] {field_name or ''} not found in sidebar.")
        return ''

    def _extract_sidebar_field(self, driver, sidebar_selector, field_selectors, attr=None, text=True, field_name=None, max_retries=3):
        """Robustly extract a field from the sidebar, waiting for presence and retrying on stale element exceptions."""
        for selector in field_selectors:
            retries = 0
            while retries < max_retries:
                try:
                    sidebar = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, sidebar_selector))
                    )
                    elem = sidebar.find_element(By.CSS_SELECTOR, selector)
                    if attr:
                        value = elem.get_attribute(attr)
                    elif text:
                        value = elem.text.strip()
                    else:
                        value = elem
                    if value:
                        print(f"[Extract] {field_name}: '{value}' (selector: {selector})")
                        return value
                    else:
                        print(f"[Extract] {field_name} empty with selector {selector}")
                        break
                except Exception as e:
                    if 'stale element reference' in str(e):
                        retries += 1
                        print(f"[Extract] {field_name} stale element, retry {retries}/{max_retries} (selector: {selector})")
                        time.sleep(0.5)
                        continue
                    else:
                        print(f"[Extract] {field_name} not found with selector {selector}: {e}")
                        break
        return ""

    def extract_sidebar_info(self, driver):
        """Extract product information from the sidebar, robustly and precisely, with explicit validation and cleaning for each field."""
        data = {"title": "", "image_url": "", "buy_now_url": "", "price": "", "url": ""}
        sidebar_selector = 'div.OCQ4zc'

        def wait_and_find(parent, selectors, attr=None, text=True, field_name=None, max_retries=3, timeout=7, validate=None, clean=None):
            for selector in selectors:
                retries = 0
                while retries < max_retries:
                    try:
                        elem = WebDriverWait(parent, timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        if attr:
                            value = elem.get_attribute(attr)
                        elif text:
                            value = elem.text.strip()
                        else:
                            value = elem
                        if clean:
                            value = clean(value)
                        if validate and not validate(value):
                            print(f"[Extract] {field_name} failed validation: '{value}' (selector: {selector})")
                            break
                        if value:
                            print(f"[Extract] {field_name}: '{value}' (selector: {selector})")
                            return value
                        else:
                            print(f"[Extract] {field_name} empty with selector {selector}")
                            break
                    except Exception as e:
                        if 'stale element reference' in str(e):
                            retries += 1
                            print(f"[Extract] {field_name} stale element, retry {retries}/{max_retries} (selector: {selector})")
                            time.sleep(0.5)
                            continue
                        else:
                            print(f"[Extract] {field_name} not found with selector {selector}: {e}")
                            break
            print(f"[Extract] {field_name} not found in sidebar.")
            return ''

        def get_sidebar():
            return WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, sidebar_selector))
            )

        # Title: Most specific, then fallback, clean whitespace
        data["title"] = wait_and_find(
            get_sidebar(),
            [
                'div.bi9tFe.PZPZlf.sjVJQd[jsname="ZOnBqe"]',
                'div[data-attrid="product_title"]',
                'div.PZPZlf[jsname="ZOnBqe"]',
                'div[role="heading"][data-attrid="product_title"]',
                'div.yYfJGb.QiH9gc.vwnbWb',
            ],
            text=True, field_name="Title",
            clean=lambda v: v.strip() if v else v,
            validate=lambda v: bool(v and len(v) > 2)
        )

        # Image URL: Only accept valid http(s) URLs, prefer product image class
        def is_valid_img_url(url):
            return url and (url.startswith('http://') or url.startswith('https://'))
        data["image_url"] = wait_and_find(
            get_sidebar(),
            [
                'img.KfAt4d[jsname="figiqf"]',
                'img.FsH7wb.wtYWhc',
                'img.VeBrne',
                'img[aria-hidden="true"]',
                'img[src^="https://encrypted-tbn"]',
            ],
            attr='src', field_name="Image URL",
            clean=lambda v: v.strip() if v else v,
            validate=is_valid_img_url
        )

        # Buy Now URL: Only accept valid http(s) URLs, prefer merchant/uchJRc links, then P9159d.hMk97e.BbI1ub, then fallbacks
        def is_valid_buy_now_url(url):
            if not url:
                return False
            # Must be a direct merchant or buy link, not a Google redirect or share link
            if url.startswith('http://') or url.startswith('https://'):
                # Exclude Google share/copy links
                if 'google.com' in url and not ('/aclk?' in url or '/shopping/product/' in url):
                    return False
                return True
            return False
        data["buy_now_url"] = wait_and_find(
            get_sidebar(),
            [
                'a.uchJRc.wDZqy',  # Most precise: main merchant buy button
                'a.P9159d.hMk97e.BbI1ub',  # Visit site button in offers
                'div.sCXXQd a.uchJRc',
                'div.XzuhHf a',
                'a.P9159d',
                'a.BbI1ub',
                'a[href*="/buy"]',
                'a[href^="http"]',
            ],
            attr='href', field_name="Buy Now URL",
            clean=lambda v: v.strip() if v else v,
            validate=is_valid_buy_now_url
        )
        data["url"] = data["buy_now_url"]

        # Price: Clean currency, only accept if contains digit, prioritize most precise selectors
        def clean_price(p):
            if not p:
                return ''
            p = p.replace('\n', ' ').replace(',', '').strip()
            # Remove any text after the price (e.g., 'Current price: ₹999')
            match = re.search(r'([₹$€£]\s?\d+[\d\s\.]*)', p)
            return match.group(1).strip() if match else p
        def is_valid_price(p):
            if not p:
                return False
            # Must contain a currency symbol and at least one digit
            return bool(re.search(r'[₹$€£]\s?\d', p))
        data["price"] = wait_and_find(
            get_sidebar(),
            [
                'span[aria-label^="Current price"]',  # Most precise: aria-label
                'div.GBgquf.JIep9e span',              # Price in offer grid
                'span.pVBUqb',                         # Price in product grid
                'div.qG8UEe',                          # Price in MRP/Total
                'span.gASiG',                          # Fallback: price span
            ],
            text=True, field_name="Price",
            clean=clean_price,
            validate=is_valid_price
        )

        # Only accept if all required fields are present and valid
        required = ["title", "image_url", "buy_now_url", "price"]
        if all(data.get(k) for k in required):
            return data
        else:
            print(f"❌ Skipping: missing one or more required fields: {data}")
            return None

    def extract_shopping_results(self, category: str) -> List[Dict]:
        """Extract shopping results by clicking products and extracting info from the sidebar only. Only accept products with all fields present, and continue until 5 complete products are found."""
        results = []
        try:
            card_selectors = [
                "li.YBo8bb",
                "div[data-merchant-id]",
                "div[data-docid]",
                ".sh-dlr__product-result",
                "[data-docid]",
                ".sh-dgr__content",
                "div[jscontroller]"
            ]
            product_cards = []
            for selector in card_selectors:
                cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if cards:
                    product_cards = cards
                    print(f"✅ Using product card selector: {selector}")
                    break
            print(f"📊 Found {len(product_cards)} product cards for {category}")
            i = 0
            found = 0
            max_attempts = len(product_cards)
            while found < 5 and i < max_attempts:
                try:
                    # Re-find product cards to avoid stale references
                    for selector in card_selectors:
                        cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if cards:
                            product_cards = cards
                            break
                    card = product_cards[i]
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                    time.sleep(random.uniform(0.5, 1.0))
                    # Click the product card to open the sidebar
                    try:
                        clickable = card
                        clickable_selectors = [
                            'div[jsaction*="click:trigger.oLMRYb"]',
                            'div[role="link"]',
                            'div',
                        ]
                        for sel in clickable_selectors:
                            try:
                                el = card.find_element(By.CSS_SELECTOR, sel)
                                if el.is_displayed() and el.is_enabled():
                                    clickable = el
                                    break
                            except:
                                continue
                        clickable.click()
                        print(f"🖱️ Clicked product card {i+1}")
                    except Exception as e:
                        print(f"⚠️ Could not click product card {i+1}: {str(e)}")
                        i += 1
                        continue
                    # Wait for sidebar to appear
                    try:
                        sidebar = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.OCQ4zc'))
                        )
                        print(f"✅ Sidebar appeared for product {i+1}")
                    except Exception as e:
                        print(f"⚠️ Sidebar did not appear for product {i+1}: {str(e)}")
                        i += 1
                        continue
                    # Extract info from sidebar only
                    data = self.extract_sidebar_info(self.driver)
                    # Only accept if all fields are present
                    if data:
                        results.append(data)
                        found += 1
                        print(f"✅ Extracted complete product {found} info from sidebar")
                    else:
                        print(f"❌ Incomplete product info, skipping. Data: {data}")
                    time.sleep(random.uniform(1, 2))
                    i += 1
                except Exception as e:
                    print(f"⚠️ Error extracting product {i+1}: {str(e)}")
                    i += 1
                    continue
        except Exception as e:
            print(f"❌ Error extracting shopping results for {category}: {str(e)}")
        return results
    
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
            self.human_like_delay(5, 8)
            
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
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_url"] = result.get('url', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_image_url"] = result.get('image_url', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_buy_now_url"] = result.get('buy_now_url', '')
                formatted_results[f"{category_prefix}_search_engine_query_result{i}_price"] = result.get('price', '')
        
        return formatted_results
    
    def run_scraper(self, input_file: str = "input.json") -> Dict:
        """Main method to run the scraper"""
        try:
            # Load input data
            with open(input_file, 'r') as f:
                input_data = json.load(f)
            data = json.loads(input_data['data'])
            queries = {
                'top_wear': data['top_wear_search_engine_query'],
                'bottom_wear': data['bottom_wear_search_engine_query'],
                'shoes': data['shoes_search_engine_query'],
                'color_recommendations': data['color_recommendations_search_engine_query']
            }
            print("🚀 Starting Google Shopping Scraper with Undetected Chrome")
            print(f"📋 Queries to scrape: {list(queries.keys())}")
            if not self.setup_driver():
                return {"error": "Failed to setup WebDriver"}
            print("⏳ Initial setup delay...")
            self.human_like_delay(8, 12)
            first = True
            for category, query in queries.items():
                print(f"\n🎯 Scraping category: {category}")
                print(f"🔍 Query: {query}")
                success = self.search_google_shopping(query, first_query=first)
                first = False
                if success:
                    print("⏳ Waiting before extraction...")
                    self.human_like_delay(5, 8)
                    results = self.extract_shopping_results(category)
                    if results:
                        self.results[category] = results
                        print(f"✅ Successfully scraped {len(results)} results for {category}")
                        print("⏳ Waiting between categories...")
                        self.human_like_delay(10, 15)
                    else:
                        print(f"⚠️ No results found for {category}")
                else:
                    print(f"⚠️ Failed to scrape {category}")
            final_results = self.format_output()
            print(f"\n✅ Scraping completed! Extracted {len(final_results)} data points")
            return final_results
        except Exception as e:
            print(f"❌ Error in main scraper: {str(e)}")
            return {"error": str(e)}
        finally:
            if self.driver:
                self.driver.quit()
                print("🖥 WebDriver closed")

    def get_xpath(self, element):
        # Helper to get XPath of a WebElement for WebDriverWait
        def get_element_xpath(el):
            path = ''
            while el is not None and el.tag_name.lower() != 'html':
                parent = el.find_element(By.XPATH, '..')
                siblings = parent.find_elements(By.XPATH, f'./{el.tag_name}')
                idx = siblings.index(el) + 1 if len(siblings) > 1 else ''
                path = f'/{el.tag_name}[{idx}]' + path
                el = parent
            return '/html' + path
        try:
            return get_element_xpath(element)
        except:
            return '.'

def run_scraper(params):
    """
    Accepts params like:
    {
        "top_wear_search_engine_query": "...",
        "bottom_wear_search_engine_query": "...",
        "shoes_search_engine_query": "...",
        "color_recommendations_search_engine_query": "..."
    }
    Returns: dict of results by category
    """
    categories = [
        "top_wear_search_engine_query",
        "bottom_wear_search_engine_query",
        "shoes_search_engine_query",
        "color_recommendations_search_engine_query"
    ]
    queries = {cat: params.get(cat) for cat in categories if params.get(cat)}
    if not queries:
        raise ValueError("No valid search queries provided in input params")
    results = {}
    for cat, query in queries.items():
        # You may need to adapt this to your scraper's API
        scraper = GoogleShoppingScraper()  # adapt as needed
        results[cat] = scraper.scrape_category(cat, query)  # adapt as needed
    return results

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