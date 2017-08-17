# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from china_paper.items import ChinaPaperItem
import urllib
import sys
import string

reload(sys)
sys.setdefaultencoding('utf-8')


class china_paper(RedisSpider):
    name = 'china_paper'
    redis_key = 'china_paper:start_urls'
    start_urls = ['http://www.paper.com.cn/']
    join_url = 'paper_industry/PaDemand.php?demandClass=2&page='
    page_num = 2604
    child_head = 'http://www.paper.com.cn'

    # lpush china_paper:start_urls http://www.paper.com.cn/

    def parse(self, response):
        print "haha:" + response.url
        for i in range(1, self.page_num):
            s = str(i)
            url = self.start_urls[0] + self.join_url + s
            yield Request(url=url, callback=self.parse_child, dont_filter=True)

    def parse_child(self, response):
        print response.url
        url_list = response.xpath(
            '//*[@id="content_disp"]/table/tr/td[2]/div[2]/table/tr[1]/td/a/@href').extract()
        for url in url_list:
            urllib_quote = urllib.quote(str(url), safe=string.printable)
            quote_split = urllib_quote.split('..')
            page_url = self.child_head + quote_split[1]
            print page_url
            yield Request(url=page_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = ChinaPaperItem()
        item["name"] = response.xpath('.//*[@id="comm_display1"]/table[1]/tr/td/div/span/span/text()').extract_first()
        item["phone"] = response.xpath(
            './/*[@id="comm_display1"]/table[2]/tr[1]/td/table/tr[1]/td[1]/div/text()').extract_first()
        item["email"] = response.xpath(
            './/*[@id="comm_display1"]/table[2]/tr[1]/td/table/tr[2]/td[1]/div/text()').extract_first()
        item["address"] = response.xpath('.//*[@id="comm_display1"]/table[2]/tr[1]/td/table/tr[3]/td/div/text()').extract_first()
        item["describe"] = response.xpath('html/body/table[4]/tbody/tr[2]/td').extract_first()
        item["product_name"] = response.xpath('.//*[@id="canshu_info"]/table/tr[1]/td[2]').extract_first()
        item["product_size"] = response.xpath('.//*[@id="canshu_info"]/table/tr[2]/td[2]').extract_first()
        item["price"] = response.xpath('.//*[@id="canshu_info"]/table/tr[4]/td[2]').extract_first()
        yield item