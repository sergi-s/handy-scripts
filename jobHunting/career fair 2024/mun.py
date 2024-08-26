import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.mun.ca/student/career-services/meet-employers/career-and-graduate-school-fair/2024-exhibitors-list/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract information from accordion-item containers
accordion_items = soup.find_all('div', class_='accordion-item')

# List to store all companies and descriptions
companies_info = []

# Define keywords related to tech or software development
tech_keywords = [
    'software', 'tech', 'technology', 'technologies', 'developer', 'engineer',
    'programming', 'IT', 'computing', 'digital', 'data', 'cyber', 'cloud',
    'AI', 'ML', 'machine learning', 'blockchain', 'web', 'internet', 'systems'
]

# Define terms to exclude from company names and descriptions
exclusion_terms = ['university', 'school', 'college', 'faculty']

# Function to check if any exclusion terms are in the text
def contains_exclusion_terms(text):
    text_lower = text.lower()
    return any(term in text_lower for term in exclusion_terms)

# Function to check if the description contains any tech-related keywords
def is_tech_company(description):
    description_lower = description.lower()
    return any(keyword in description_lower for keyword in tech_keywords)

# Handle accordion-item containers
for item in accordion_items:
    company_name_tag = item.find('div', class_='accordion-item-link-wrapper').find('a')
    company_name = company_name_tag.get_text(strip=True)

    description_tag = item.find('div', class_='accordion-item-content')
    description = description_tag.get_text(strip=True) if description_tag else "No description available"

    # Check if company should be excluded
    if contains_exclusion_terms(company_name) or contains_exclusion_terms(description):
        continue

    companies_info.append((company_name, description))

# Filter and print companies that match the tech-related keywords
tech_companies = [(name, desc) for name, desc in companies_info if is_tech_company(desc)]

print("Tech Companies:")
for company_name, description in tech_companies:
    print(f"Company: {company_name}")
    # print(f"Description: {description}\n")
