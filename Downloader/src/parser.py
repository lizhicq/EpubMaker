from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
from Downloader.src.cleaner import remove_ads_words

def get_html_from_url(url,headless=True):
    # Set up Chrome options
    chrome_options = Options()
    if headless == True:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
    chrome_options.binary_location = (
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    )

    # Initialize a Chrome webdriver
    # $xattr -d com.apple.quarantine chromedriver 
    driver = webdriver.Chrome(
        executable_path=os.getenv('CHROMEDRIVER_PATH'), 
        options=chrome_options
    )
    # Load the page
    driver.get(url)

    # Get the source HTML of the page
    html = driver.page_source

    # Close the browser
    driver.quit()

    return html

def get_novel_chapters(content_url:str):
    # Replace 'html_content' with your actual HTML content string
    max_retry = 10
    retry = 0
    html_content = ''
    while len(html_content) < 10 and retry < max_retry:
        html_content = get_html_from_url(content_url, headless=False)
    
    # Using BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Finding all <a> tags within <li> tags
    chapter_list = soup.find_all('li')

    # Extracting chapter names and URLs
    chapters = []
    for index, chapter in enumerate(chapter_list):
        link = chapter.find('a')
        if link and 'href' in link.attrs:
            chapter_url = content_url + "/" + link['href'].strip()
            chapter_title = str(index) + '-' + (link.text.strip() or "bad chapter")
            chapter_title = chapter_title[:14]
            chapter_info = {
                'title': chapter_title, 
                'url': chapter_url,
                'content':""
            }
            chapters.append(chapter_info)
    return chapters


def extract_novel_chapter(chapter_url):
    chapter_html = get_html_from_url(chapter_url, headless=False)
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(chapter_html, 'html.parser')
    # 获取 id 为 'content' 的 div 标签的内容
    content_div = soup.find('div', {'id': 'content'})

    # 获取 class 为 'contentadv' 的 div 标签内容
    content_adv_div = soup.find('div', {'class': 'contentadv'})

    full_text = ""
    # 提取并合并两个部分的纯文本内容
    if content_div:
        content_text = content_div.get_text(separator="\n", strip=True)
        full_text += content_text
        
    if content_adv_div:
        content_adv_text = content_adv_div.get_text(separator="\n", strip=True)
        full_text += content_adv_text
    
    return remove_ads_words(full_text)
