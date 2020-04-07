# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['http://qiushibaike.com/text/page/1/']
    baseDomain = 'https://www.qiushibaike.com'

    def parse(self, response):
        duanzidivs = response.xpath('//div[@class="col1 old-style-col1"]/div')
        for duanzidiv in duanzidivs:
            author = duanzidiv.xpath('.//h2/text()').get().strip()
            content = duanzidiv.xpath('.//div[@class="content"]//text()').getall()
            content = ''.join(content).strip()
            item = QsbkItem(author=author, content=content)
            yield item
            nextUrl = duanzidiv.xpath('//ul[@class="pagination"]/li[last()]/a/@href').get()
            if not nextUrl:
                return
            else:
                yield scrapy.Request(self.baseDomain + nextUrl, callback=self.parse)


