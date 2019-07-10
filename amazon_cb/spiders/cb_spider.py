import scrapy

class MySpider(scrapy.Spider):
    name="cb_spider"

    def start_requests(self):
        urls=[
            "https://www.amazon.com/s?k=SMARTPHONE&ref=nb_sb_noss_2",

        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):

        containers=response.css("div.sg-col-20-of-24.s-result-item.sg-col-0-of-12.sg-col-28-of-32.sg-col-16-of-20.sg-col.sg-col-32-of-36.sg-col-12-of-16.sg-col-24-of-28")
        for container in containers:
            text=container.css("span.a-size-medium.a-color-base.a-text-normal::text").get()
            price=container.css("span.a-price-symbol::text").get()+container.css("span.a-price-whole::text").get()
            tags=container.css("span.a-icon-alt::text").get()

            yield{
                "Info of the Phone":text,
                "Price":price,
                "Ratings":tags
            }
            next_page_id = response.css("li.a-last a::attr(href)").get()
            if next_page_id[-1] is not "6":
                next_page=response.urljoin(next_page_id)
                yield scrapy.Request(next_page,callback=self.parse)