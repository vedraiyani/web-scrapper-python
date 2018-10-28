# Target dataset path
DATASET_PATH = "./dataset"

# Fake user agent for avoiding 503 error
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
}

# Base url of scrapping
BASE_URL = "https://burst.shopify.com"

# Advanced parameters
# Categories want to scrap
CATEGORIES = ["dog","cat"]

# Page limit to search images from URL
PAGE_FROM =1
PAGE_TO = 2

# Number of workers for downloading pages and images for better and faster performance
WORKERS = 4
