import os
import json
import csv
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables from .env file
load_dotenv()

def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")

    wait = WebDriverWait(driver, 10)
    email_element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    password_element = driver.find_element(By.ID, 'password')

    email_element.send_keys(username)
    password_element.send_keys(password)
    
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    wait.until(EC.url_changes("https://www.linkedin.com/login"))

def parse_company_size(size_text):
    # Remove any non-numeric characters except for the dash
    size_text = re.sub(r'[^\d-]', '', size_text)
    # Extract numeric values from size text
    match = re.search(r'(\d+)-(\d+)', size_text)
    if match:
        return match.group(1) + "-" + match.group(2)
    return None

def get_company_info(driver, linkedin_url):
    if not linkedin_url.endswith('/about'):
        linkedin_url = linkedin_url.rstrip('/') + '/about'
    
    driver.get(linkedin_url)

    wait = WebDriverWait(driver, 10)
    company_size = None
    industry = None
    phone = None
    associated_members = None
    connections = 0

    try:
        size_selectors = [
            'dd.t-black--light.text-body-medium.mb1',
            'dd.t-black--light.text-body-medium.mb4'
        ]
        
        size_element = None
        for selector in size_selectors:
            try:
                size_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                if size_element:
                    break
            except:
                continue
        
        if size_element:
            company_size_text = size_element.text.strip()
            company_size = parse_company_size(company_size_text)
        else:
            print(f"No company size element found for {linkedin_url}")
    except Exception as e:
        print(f"Error retrieving company size from {linkedin_url}")

    try:
        industry_label = driver.find_element(By.XPATH, "//dt[h3[text()='Industry']]//following-sibling::dd")
        industry = industry_label.text
    except Exception as e:
        print(f"Error retrieving industry from {linkedin_url}")

    try:
        phone_label = driver.find_element(By.XPATH, "//dt[h3[text()='Phone']]//following-sibling::dd")
        phone_element = phone_label.find_element(By.TAG_NAME, 'a')
        phone_span = phone_element.find_element(By.CSS_SELECTOR, 'span[aria-hidden="true"]')
        phone = phone_span.text.strip()
    except Exception as e:
        pass

    try:
        connections_element = driver.find_element(By.CSS_SELECTOR, 'h2.t-black.link-without-visited-state.text-body-small-bold')
        connections_text = connections_element.text
        connections_match = re.search(r'(\d+) other connection[s]?', connections_text)
        if connections_match:
            connections = int(connections_match.group(1)) + 1
    except Exception as e:
        print(f"Error retrieving connections from {linkedin_url}")
    
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, 'dd.t-black--light.mb4.text-body-medium a span')
        associated_members = None
        for element in elements:
            associated_members_text = element.text
            members_match = re.search(r'(\d+) associated member[s]?', associated_members_text)
            if members_match:
                associated_members = int(members_match.group(1))
                break
    except Exception as e:
        print(f"Error retrieving associated members")

    return {
        "Company Size": company_size,
        "Industry": industry,
        "Phone": phone,
        "Connections": connections,
        "Associated Members": associated_members
    }

def main():
    json_file_name = "company_info.json"
    csv_file_name = os.path.splitext(json_file_name)[0] + ".csv"

    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        username = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not username or not password:
            raise ValueError("LinkedIn email and password environment variables must be set.")

        linkedin_login(driver, username, password)

        # Load the JSON file
        with open(json_file_name, 'r') as file:
            data = json.load(file)

        # Prepare CSV data
        csv_data = []
        for company in data:
            linkedin_url = company.get('LinkedIn')
            if linkedin_url:
                company_info = get_company_info(driver, linkedin_url)
                company.update(company_info)
                csv_data.append(company)

        # Write to CSV file
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(csv_data[0].keys()))
            writer.writeheader()
            writer.writerows(csv_data)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
