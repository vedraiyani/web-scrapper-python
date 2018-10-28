import scrapy

"""
    Abstraction of Blog Scrapper
"""
class BlogSpider(scrapy.Spider):
    # configure name of blog spider and URL
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    """
        Implement parser 
    """
    def parse(self, response):
        # extract titles from page
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').extract_first()}

        # move to the next page
        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)