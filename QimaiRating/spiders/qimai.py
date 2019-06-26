# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_splash import SplashRequest

most_help = """
  js = string.format("document.querySelector('#app-comment > div.comment-details > div.filter-container > div:nth-child(2) > div:nth-child(1) > div.filter-content > ul > li:nth-child(2) > a').click();", args.page)
  splash:runjs(js)
  assert(splash:wait(args.wait))
"""


page_no_lua = """
function main(splash, args)
  splash.images_enabled = true
  assert(splash:go(args.url))
  assert(splash:wait(args.wait))
  %s
  js = string.format("document.querySelector('.ivu-page > li:nth-child(%d) > a').click();", args.page)
  splash:runjs(js)
  assert(splash:wait(args.wait))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""


class QimaiSpider(scrapy.Spider):
    name = 'qimai'
    allowed_domains = ['qimai.cn']
    # 'https://www.qimai.cn/app/comment/appid/414478124/country/cn',
    url = 'https://www.qimai.cn/app/comment/appid/1084660392/country/cn'
    page_no = 2
    query_type = ""

    def start_requests(self):
        yield SplashRequest(self.url, self.parse, endpoint="execute",
                            args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url, 'wait': 5})

    def parse(self, response):
        app_name = response.xpath('//div[@class="appname"]/text()').extract_first()
        app_author = response.xpath('//div[@class="auther"]/div/div/div[@class="value"]/text()').extract_first()
        app_id = response.xpath('//div[@class="appid"]/div[@class="value"]/a/text()').extract_first()
        app_price = response.xpath('//div[@class="price"]/div[@class="value"]/text()').extract_first()
        app_last_version = response.xpath('//div[@class="version"]/div[@class="value"]/text()').extract_first()
        next_text = response.xpath('//li[@class="ivu-page-next ivu-page-disabled"]/@title').extract_first()
        page_no_list = response.xpath('//ul[@class="ivu-page"]/li').extract()
        li_page = Selector(text=page_no_list[-2])
        page_no = li_page.xpath('.//a/text()').extract_first()
        print(app_name.strip(), app_author, app_id, app_price, app_last_version.strip(), next_text, page_no)
        score_list = response.xpath('//div[@class="score-box"]').extract()
        for score in score_list:
            div_score = Selector(text=score)
            score_header = div_score.xpath('.//div[@class="score-header"]/text()').extract_first()
            score_star = div_score.xpath('.//div[@class="score-star"]/p[@class="num"]/text()').extract_first()
            comment_num = div_score.xpath(
                './/div[@class="score-star"]/p[@class="comment-num-item"]/text()').extract_first()
            print(score_header, score_star, comment_num)

        tr_list = response.xpath('//tbody[@class="ivu-table-tbody"]/tr').extract()
        for tr in tr_list:
            tr_comment = Selector(text=tr)
            rate = tr_comment.xpath('.//input/@value').extract_first()
            title = tr_comment.xpath('.//p[@class="title"]/span/text()').extract_first()
            content = tr_comment.xpath('.//div[@class="body"]/span/text()').extract_first()
            author = tr_comment.xpath('.//span[@class="author"]/a/text()').extract_first()
            author_href = tr_comment.xpath('.//span[@class="author"]/a/@href').extract_first()
            publish_time = tr_comment.xpath('.//td/div/span/text()').extract_first()
            deleted = tr_comment.xpath('.//i[@style="display:inline-block"]/text()').extract_first()
            print(rate, title, content, author, author_href, deleted, publish_time)
        if next_text is None:
            self.page_no += 1
            yield SplashRequest(self.url, self.parse_comment, endpoint="execute",
                                args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url, 'wait': 5})
        else:
            yield {}

    def parse_comment(self, response):
        next_text = response.xpath('//li[@class="ivu-page-next ivu-page-disabled"]/@title').extract_first()
        print(next_text)
        tr_list = response.xpath('//tbody[@class="ivu-table-tbody"]/tr').extract()
        for tr in tr_list:
            tr_comment = Selector(text=tr)
            rate = tr_comment.xpath('.//input/@value').extract_first()
            title = tr_comment.xpath('.//p[@class="title"]/span/text()').extract_first()
            content = tr_comment.xpath('.//div[@class="body"]/span/text()').extract_first()
            author = tr_comment.xpath('.//span[@class="author"]/a/text()').extract_first()
            author_href = tr_comment.xpath('.//span[@class="author"]/a/@href').extract_first()
            publish_time = tr_comment.xpath('.//td/div/span/text()').extract_first()
            deleted = tr_comment.xpath('.//i[@style="display:inline-block"]/text()').extract_first()
            print(rate, title, content, author, author_href, deleted, publish_time)
        if next_text is None and self.page_no < 4:
            self.page_no += 1
            yield SplashRequest(self.url, self.parse_comment, endpoint="execute",
                                args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url, 'wait': 5})
        elif self.query_type.__len__() == 0:
            self.page_no = 2
            self.query_type = most_help
            yield SplashRequest(self.url, self.parse_comment, endpoint="execute",
                                args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url,
                                      'wait': 5})
        else:
            yield {}
