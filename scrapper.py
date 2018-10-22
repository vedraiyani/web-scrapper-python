import os

from config import *
from lib.beutiful_scrapper import Scrapper

# initialize scrapper
scrapper = Scrapper()

# Loop through categories
for category in CATEGORIES:
    target_path = os.path.join(DATASET_PATH, category)
    scrapper.set_target_path(target_path)

    url = BASE_URL + "/" + category + "?page=0"

    list_of_urls = []
    # Loop through number of pages
    for page_number in range(PAGE_FROM,PAGE_TO):
        url_with_page_number = url.replace("page=0","page="+str(page_number))
        list_of_urls.append(url_with_page_number)

    # get all HTML
    features = scrapper.scrap(list_of_urls)




