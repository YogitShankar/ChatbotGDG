import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from config import BASE_DIR
from bs4 import BeautifulSoup
import sys

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
url="https://codeforces.com/contest/1946/problem/A"
driver.get(url)
problem_number=url.split("/")[-3]
problem_alphabet=url.split("/")[-1]

try:
    link = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Tutorial (en)"))
    )
    link.click()

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  
    windows = driver.window_handles
    driver.switch_to.window(windows[1])

    spoiler_title = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//b[contains(text(), "Editorial")]'))
    )
    spoiler_title.click()
    editorial_content = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@class="spoiler-content"]'))
    )
    sys.stdout.reconfigure(encoding='utf-8')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    editorial_div = soup.find('div', class_='spoiler-content')
    if editorial_div:
        paragraphs = editorial_div.find_all('p')  
        editorial_text = "\n".join([p.get_text() for p in paragraphs])  
        dir_name=f"{problem_number}{problem_alphabet}"
        dir=os.path.join(BASE_DIR,"data","editorials")
        os.makedirs(dir, exist_ok=True)
        file_path = os.path.join(dir, f"{dir_name}.txt")
        with open(file_path,'w',encoding="utf-8") as f:
            f.write(editorial_text)
    else:
        print("Editorial content not found!")

    

except Exception as e:
    print(e)

finally:
    time.sleep(2)
    driver.quit()
