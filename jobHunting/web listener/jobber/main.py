import requests
from bs4 import BeautifulSoup
import re
import subprocess

# Define the function for desktop notifications using AppleScript
def send_notification(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(['osascript', '-e', script])

# URL of the careers page
url = 'https://getjobber.com/about/careers/'

# Set up headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

# Send a GET request to the webpage
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the specific div with id "product-software-engineering"
    product_engineering_div = soup.find('div', id='product-software-engineering')

    # Check if the div was found
    if product_engineering_div:
        # Find all job listing posts within this div
        jobs = product_engineering_div.find_all('div', class_='wp-block-jobber-job-list__post')

        # Define keywords for checking job titles
        keywords = ['co-op', 'intern', 'internship', 'apprenticeship']

        # Compile a regular expression pattern for case-insensitive matching
        pattern = re.compile('|'.join(keywords), re.IGNORECASE)

        # Loop through the job listings and print those with matching titles
        for job in jobs:
            title = job.find('a').get_text(strip=True)

            # Check if the title contains any of the keywords
            if pattern.search(title):
                print(title)
                send_notification("Found A job in Jobber", f"A new job listing matching your criteria was found: {title}")
    else:
        print("The specified div with id 'product-software-engineering' was not found.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
