from bs4 import BeautifulSoup
import concurrent.futures
import os
import ssl
import urllib.request



from config import *

"""
    Abstraction for scrapping
"""


class Scrapper:
    """
        Set target_path and create destination directories
        :param target_path : Target specified path for downloading images
    """

    def set_target_path(self, target_path):
        self.target_path = target_path
        self._create_dirs()

    """
        Fetch HTML of specified url and parse
        :param page_url: URL of HTML page
    """

    def url_to_html_parser(self, url, timeout):
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout, context=context) as response:
            html = response.read()
            return BeautifulSoup(html, "html.parser")

    """
        Scrap URLs in multi-thread env.
        :param list_of_urls: List of urls needs to be downloaded.
    """

    def scrap(self, list_of_urls):
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(self.url_to_html_parser, url, 60): url for url in list_of_urls}
            for future in concurrent.futures.as_completed(future_to_url):
                handler = future.result()
                self.fetch_images(handler)

    """
        Download Items from specified page
        :param handler: soap handler that finds elements from page source
    """

    def fetch_images(self, handler):

        # find list of grids
        grids = handler.select('.photo-tile__image-wrapper')

        # extract URLs from grids
        image_urls = self.extract_image_urls(grids)

        # download images
        self.download_images(image_urls, 60)

    """
        Extract image URLs from grid
        :param grids: list of grids
    """

    def extract_image_urls(self, grids):
        extracted_urls = []
        # loop through grids and find images
        for grid in grids:
            # fetch image tags from grid
            images = grid.select("img")
            # extract URLS from images
            for image in images:
                # get data property
                image_urls = image.get('data-srcset')
                image_urls = image_urls.split(',')
                # fetch high resolution image URL
                high_resolution_pair = image_urls[-1].split(' ')
                high_resolution_image_url = high_resolution_pair[1].replace("@2x", "@3x")
                if high_resolution_image_url is not None:
                    extracted_urls.append(high_resolution_image_url)

        return extracted_urls

    """
        Download images from 
    """

    def download_images(self, image_urls, timeout):
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(self.download_image, url, timeout): url for url in image_urls}
            count_images = 0
            for future in concurrent.futures.as_completed(future_to_url):
                files = future.result()
                count_images = count_images + len(files)

            print("%d images downloaded to %s" % (count_images, self.target_path))

    """
        Download single image from specified URL
        :param image_url: Image URL of image
        :param timeout: timeout for downloading image
    """

    def download_image(self, image_url, timeout):
        files = []
        # extract name of file from URL
        file_name = image_url.split("/")[-1]

        # build target path of image
        image_path = os.path.join(self.target_path, file_name)

        # write image to file system
        if not os.path.exists(image_path):
            with open(image_path, 'wb') as f:
                f.write(self._read_image(image_url, timeout))
                files.append(file_name)
                f.close()

        return files

    """
       Read image from specified URL
       :param image_url: URL of image
    """

    def _read_image(self, image_url, timeout):
        context = ssl._create_unverified_context()
        req = urllib.request.Request(image_url, headers=HEADERS)
        response = urllib.request.urlopen(req, timeout=timeout, context=context)
        return response.read()

    """
        Create all directories before downloading images
    """

    def _create_dirs(self):
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)
