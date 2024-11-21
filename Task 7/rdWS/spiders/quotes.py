import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    current = 0
    max_page = 1
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.xpath("span/small/text()").get()
                }
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None and self.current < self.max_page:
            self.current += 1
            yield response.follow(next_page, callback=self.parse)
