import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = 'https://www.getcoding.ca/survey-nl'

# Function to fetch and parse HTML from a URL
def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request was unsuccessful
    return response.text

# Function to extract company information from HTML
def extract_company_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    company_info = []
    
    # Find all company sections
    for item in soup.find_all('div', class_='surveyitem w-dyn-item'):
        # Extract company name
        company_name = item.find('h4', class_='company-name').text.strip()
        
        # Extract LinkedIn profile and website
        social_media_links = item.find_all('a', class_='card-teacher-social-media-link')
        linkedin = None
        website = None
        for link in social_media_links:
            href = link.get('href')
            if 'linkedin.com' in href:
                linkedin = href
            elif 'http' in href:
                website = href
        
        # Extract technologies
        technologies = {}
        for section in item.find_all('div', class_='comparison-wrap bottom'):
            for heading in section.find_all('h4', class_='comparsion-heading technologies'):
                tech_category = heading.text.strip()
                # Find the corresponding <p> tag for this category
                tech_paragraph = heading.find_next_sibling('p', class_='comparsiontext technologies')
                if tech_paragraph:
                    tech_list = tech_paragraph.text.strip()
                    technologies[tech_category] = [tech.strip() for tech in tech_list.split(',')]
        
        company_info.append({
            'Company Name': company_name,
            'LinkedIn': linkedin,
            'Website': website,
            'Technologies': technologies
        })
    
    return company_info

# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    html_content = fetch_html(url)
    info = extract_company_info(html_content)
    
    # Save the extracted company information to a JSON file
    save_to_json(info, 'company_info.json')
    print("Data has been saved to 'company_info.json'")

if __name__ == '__main__':
    main()
