import concurrent.futures
import os
import ssl
import urllib.request


"""
    Abstraction of Utils
"""
class Utils:


    """
        Download images from specified URLs
        image_urls: list of image URLs to download
        timeout: timeout to download image
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