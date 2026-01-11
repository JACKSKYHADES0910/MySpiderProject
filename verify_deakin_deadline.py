from selenium import webdriver
from spiders.australia.deakin_spider import DeakinSpider
import time

def test_extraction():
    # Setup spider
    spider = DeakinSpider(headless=False)
    
    try:
        url = "https://www.deakin.edu.au/course/graduate-certificate-criminology#banner"
        print(f"Testing URL: {url}")
        
        # Initialize driver manually for testing
        spider._driver = webdriver.Chrome()
        spider.driver.get(url)
        
        # Wait for page load
        time.sleep(5)
        
        # Test extraction
        print("\n--- Testing _extract_key_dates ---")
        result = spider._extract_key_dates(spider.driver)
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if spider.driver:
            spider.driver.quit()

if __name__ == "__main__":
    test_extraction()
