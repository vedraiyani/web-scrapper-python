from selenium import webdriver

from bs4 import BeautifulSoup
import os
import urllib.request
from tqdm import tqdm
import ssl

from config import *

# Configure some static
timeout = 60 # Request timeout
url = BASE_URL + "/cat" # URL being scrapped
target_dir = os.path.join(DATASET_PATH,"cat") # Target directory for scrapping data

# Use selenium firefox driver to get page source
browser = webdriver.Firefox()
browser.get(url)

# get page source
html = browser.page_source


# Parse HTML source using BeautifulSoup
soup =  BeautifulSoup(html, "html.parser")

# Find list of grids
image_grids = soup.select('.js-track-photo-stat-view')

# Loop through grids and stack URLs
image_urls = []
for image_tag in tqdm(image_grids,desc="Find Images"):

    # Fetch data tag which includes sequence of URLS
    image_url = image_tag.get('data-srcset')

    # Extract highest resolution image from data tad
    image_url = image_url.split(',')
    high_resolution_pair = image_url[-1].split(' ')
    high_resolution_image_url = high_resolution_pair[1].replace("@2x", "@3x")

    # Stack all image urls
    image_urls.append(high_resolution_image_url)

# Download images into target directory
for image_url in tqdm(image_urls,desc="Download Images"):

    # Extract name of file from URL
    file_name = image_url.split("/")[-1]

    # Build target path of image
    image_path = os.path.join(target_dir, file_name)

    # Create directories
    if not os.path.exists(target_dir): os.mkdir(target_dir)

    # Write image to file system
    if not os.path.exists(image_path):

        # Read image from web
        req = urllib.request.Request(image_url, headers=HEADERS)
        response = urllib.request.urlopen(req, timeout=timeout, context=context)

        # Write it down to file system
        f = open(image_path, 'wb')
        f.write(response.read())
        f.close()




