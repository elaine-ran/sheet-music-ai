import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL of the Wikipedia page
url = "https://en.wikipedia.org/w/index.php?title=Category:Composers_for_piano&pageuntil=Kalivoda%2C+Jan%0AJan+Kalivoda#mw-pages"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Print the title of the page
    print(soup.title.string)
    
    # Find and print all the links in the category page
    for link in soup.find_all('a'):
        print(link.get('href'))
else:
    print("Failed to retrieve the page")

# Optionally, you can save the HTML content to a file
with open('wikipedia_composers_for_piano.html', 'w', encoding='utf-8') as file:
    file.write(response.text)
