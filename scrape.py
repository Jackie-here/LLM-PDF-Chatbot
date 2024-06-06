import requests
from bs4 import BeautifulSoup

website_url = "https://avibase.bsc-eoc.org/checklist.jsp?lang=EN&p2=1&list=clements&synlang=&region=HK&version=images&lifelist=&highlight=0"  # Replace with the website URL you want to scrape

# Send a GET request to the website and retrieve the HTML content
response = requests.get(website_url)
html_content = response.content

#print(html_content)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract relevant data such as text, image URLs, and sounds using BeautifulSoup methods
text_data = soup.get_text()
image_urls = [img['src'] for img in soup.find_all('img')]

print(text_data)
print(image_urls)