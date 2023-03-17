from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse
from typing import Dict
from bs4 import BeautifulSoup

# call: scrapy runspider wiki_scraper.py -o wiki.jsonl


class MySpider(CrawlSpider):
    name = "wiki_spider"
    start_urls = ["https://en.wikipedia.org/wiki/FIFA_World_Cup"]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=[
                    "https://en.wikipedia.org/wiki/FIFA_World_Cup",
                ],
                deny_domains=[],
                deny=[],
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response: HtmlResponse) -> Dict:
        item = dict()
        item["url"] = response.url
        item["title"] = response.meta["link_text"].strip()
        # TODO: check how to best extract wiki content
        soup = BeautifulSoup(response.body, "html.parser")
        item["content"] = "\n".join(
            [h.text.strip() for h in soup.find_all("h1", "h2", "h3", "h4", "h5", "p")]
        )
        return item
