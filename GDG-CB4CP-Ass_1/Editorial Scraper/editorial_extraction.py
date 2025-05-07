import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import os

# Set up Selenium WebDriver
driver_path = '/Users/shivalasya/Desktop/chatbot/chromedriver-mac-arm64/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Prepare output directories
text_output_dir = "./data/editorial"
os.makedirs(text_output_dir, exist_ok=True)
try:
    # Open the target URL
    url = "https://codeforces.com/blog/entry/128716"
    driver.get(url)

    # Wait for the page to load dynamically
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Find the specific href section
    target_href = "/contest/1957/problem/A"
    target_element = driver.find_element(By.XPATH, f"//a[@href='{target_href}']")
    if target_element:
        # Scroll to the element
        ActionChains(driver).move_to_element(target_element).perform()

        # Extract the surrounding content
        parent_div = target_element.find_element(By.XPATH, "./ancestor::div")
        soup = BeautifulSoup(parent_div.get_attribute("innerHTML"), 'html.parser')

        # Initialize a dictionary to store extracted data
        extracted_data = {}

        # Extract Hint 1
        hint_title = soup.find("b", string="Hint 1")
        if hint_title:
            hint_content = hint_title.find_next("div", class_="spoiler-content")
            extracted_data["Hint 1"] = hint_content.text.strip() if hint_content else "No Hint 1 found."

        # Extract Solution
        solution_title = soup.find("b", string="Solution")
        if solution_title:
            solution_content = solution_title.find_next("div", class_="spoiler-content")
            extracted_data["Solution"] = solution_content.text.strip() if solution_content else "No Solution found."

        # Extract "Rate this Problem"
        rate_title = soup.find("b", string="Rate this problem")
        if rate_title:
            rate_section = rate_title.find_next("div", class_="spoiler-content")
            if rate_section:
                rates = {}
                rate_items = rate_section.find_all("li")
                for rate in rate_items:
                    rate_label = rate.find("span").text.strip() if rate.find("span") else "Unknown"
                    rate_value = rate.find("span", class_="likeCount")
                    rate_value = rate_value["data-value"] if rate_value else "N/A"
                    rates[rate_label] = rate_value
                extracted_data["Rate this Problem"] = rates
            else:
                extracted_data["Rate this Problem"] = "No Rate this Problem section found."

        # Extract C++ Code
        cpp_code_title = soup.find("b", string="C++ Code")
        if cpp_code_title:
            cpp_code_content = cpp_code_title.find_next("pre")
            extracted_data["C++ Code"] = html.unescape(cpp_code_content.text.strip()) if cpp_code_content else "No C++ Code found."

        # Save extracted content
        
        problem_filename = os.path.join(text_output_dir, f"editorial_1957A.txt")
        with open(problem_filename, "w", encoding="utf-8") as f:
        
            for key, value in extracted_data.items():
                # print(f"{key}:")
                f.write(f"{key}:\n")
                if isinstance(value, dict):  
                    for sub_key, sub_value in value.items():
                        # print(f"  {sub_key}: {sub_value}")
                        f.write(f"  {sub_key}: {sub_value}\n")
                else:
                    # print(f"{value}")
                    f.write(f"{value}\n")
                # print()
                f.write("\n")
    else:
        print(f"No section found for href='{target_href}'.")

finally:
    # Close the driver
    driver.quit()

