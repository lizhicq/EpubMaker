from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# 配置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 设置 WebDriver
driver = webdriver.Chrome(
        executable_path=os.getenv('CHROMEDRIVER_PATH'),
        options=chrome_options
    )

# 加载网页
driver.get("https://www.piaotia.com/html/14/14836/")

try:
    # 等待包含目标文本的 <a> 元素出现
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//li/a[contains(text(), '第1009章 两处')]")
        )
    )

    # 获取页面源代码
    html = driver.page_source
    print(html)
finally:
    driver.quit()
