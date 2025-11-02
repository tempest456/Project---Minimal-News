import scrapy
from scrapy.crawler import CrawlerProcess
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models import News
from .scrape import scrape_article
from .summarizer import summarize


class EkantipurSpider(scrapy.Spider):
    name = 'enews'
    category = ['world', 'business', 'sports',
                'entertainment', 'science-technology']

    start_urls = [
        'https://thehimalayantimes.com/category/nepal'
    ]

    def parse(self, response):
        post = response.css('.col-sm-8 li')
        for i in range(3):
            headline = post.css('a::attr(title)')[i].get()
            link = post.css('a::attr(href)')[i].get()
            category = link.split('/')[3]
            summary = summarize(scrape_article(link))
            news = News(headline=headline, url=link, summarized_body=summary,
                        category=category)
            db.session.add(news)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        for objects in EkantipurSpider.category:
            next_page = f'https://thehimalayantimes.com/category/{objects}/'
            yield response.follow(next_page, callback=self.parse)

def run_spider():
    process = CrawlerProcess()
    process.crawl(EkantipurSpider)
    process.start()
