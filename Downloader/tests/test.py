from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os 
def get_html_from_url(url):    
    # Set up Chrome options
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")

    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
    chrome_options.binary_location = (
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    )

    # Test Options
    #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_options.add_experimental_option("useAutomationExtension", False)

    # Initialize a Chrome webdriver
    # $xattr -d com.apple.quarantine chromedriver 
    driver = webdriver.Chrome(
        executable_path=os.getenv('CHROMEDRIVER_PATH'), 
        options=chrome_options
    )
    
    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Load the page
    driver.get(url)

    # Get the source HTML of the page
    html = driver.page_source

    # Close the browser
    driver.quit()

    return html

if __name__ == "__main__":
    url = "https://www.piaotian.com/html/9/9130/"
    html = get_html_from_url(url)
    print(html)