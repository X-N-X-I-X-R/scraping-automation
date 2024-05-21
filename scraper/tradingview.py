import scrapy
from scrapy.crawler import CrawlerProcess
import os

class MyNewsSpider(scrapy.Spider):
    name = "mynews_spider"
    allowed_domains = ["tradingview.com"]
    start_urls = ["https://www.tradingview.com/news/"]

    def parse(self, response):
        for news_article in response.css(".news-article"):
            title = news_article.css(".news-title::text").get()
            content = news_article.css(".news-content").get()
            date = news_article.css(".news-date::text").get()
            save_to = os.path.join(settings.BASE_DIR, 'scraper', 'saved_data')
            if title and content and date:
              save_to = os.path.join(save_to, f"{title}.html")
              print(f"{title}Saving to {save_to}")
                

            yield {
                "title": title,
                "content": content,
                "date": date
            }

        next_page_url = response.css(".next-page a::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(next_page_url)

process = CrawlerProcess()
process.crawl(MyNewsSpider)
process.start()
