# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_splash import SplashRequest

from QimaiRating.items import CommentInfoItem, RateInfoItem, AppInfoItem

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
    app_info = AppInfoItem()

    def start_requests(self):
        yield SplashRequest(self.url, self.parse, endpoint="execute",
                            args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url,
                                  'wait': 5})

    def parse(self, response):
        self.app_info['type'] = 0
        self.app_info['app_name'] = response.xpath('//div[@class="appname"]/text()').extract_first().strip()
        self.app_info['app_author'] = response.xpath(
            '//div[@class="auther"]/div/div/div[@class="value"]/text()').extract_first()
        self.app_info['app_id'] = response.xpath('//div[@class="appid"]/div[@class="value"]/a/text()').extract_first()
        self.app_info['app_price'] = response.xpath('//div[@class="price"]/div[@class="value"]/text()').extract_first()
        self.app_info['app_last_version'] = response.xpath(
            '//div[@class="version"]/div[@class="value"]/text()').extract_first().strip()

        next_text = response.xpath('//li[@class="ivu-page-next ivu-page-disabled"]/@title').extract_first()
        score_list = response.xpath('//div[@class="score-box"]').extract()
        for score in score_list:
            div_score = Selector(text=score)
            rate_info = RateInfoItem()
            rate_info['type'] = 1
            rate_info['score_header'] = div_score.xpath('.//div[@class="score-header"]/text()').extract_first()
            rate_info['score_star'] = div_score.xpath(
                './/div[@class="score-star"]/p[@class="num"]/text()').extract_first()
            rate_info['comment_num'] = div_score.xpath(
                './/div[@class="score-star"]/p[@class="comment-num-item"]/text()').extract_first()
            yield rate_info

        tr_list = response.xpath('//tbody[@class="ivu-table-tbody"]/tr').extract()
        for tr in tr_list:
            tr_comment = Selector(text=tr)
            comment_info = CommentInfoItem()
            comment_info['title'] = tr_comment.xpath('.//p[@class="title"]/span/text()').extract_first()
            comment_info['author'] = tr_comment.xpath('.//span[@class="author"]/a/text()').extract_first()
            comment_info['content'] = tr_comment.xpath('.//div[@class="body"]/span/text()').extract_first()
            comment_info['author_href'] = "https://www.qimai.cn" + (
                tr_comment.xpath('.//span[@class="author"]/a/@href').extract_first())
            comment_info['rate'] = tr_comment.xpath('.//input/@value').extract_first()
            comment_info['publish_time'] = tr_comment.xpath('.//td/div/span/text()').extract_first()
            comment_info['deleted'] = tr_comment.xpath('.//i[@style="display:inline-block"]/text()').extract_first()
            if self.query_type.__len__() == 0:
                comment_info['type'] = 2
            else:
                comment_info['type'] = 3
            yield comment_info
        if next_text is None and self.page_no < 2:
            self.page_no += 1
            yield SplashRequest(self.url, self.parse_comment, endpoint="execute",
                                args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url,
                                      'wait': 5})
        elif self.query_type.__len__() == 0:
            self.page_no = 2
            self.query_type = most_help
            yield SplashRequest(self.url, self.parse_comment, endpoint="execute",
                                args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url,
                                      'wait': 5})
        else:
            yield self.app_info

    def parse_comment(self, response):
        next_text = response.xpath('//li[@class="ivu-page-next ivu-page-disabled"]/@title').extract_first()
        tr_list = response.xpath('//tbody[@class="ivu-table-tbody"]/tr').extract()
        for tr in tr_list:
            tr_comment = Selector(text=tr)
            comment_info = CommentInfoItem()
            comment_info['title'] = tr_comment.xpath('.//p[@class="title"]/span/text()').extract_first()
            comment_info['author'] = tr_comment.xpath('.//span[@class="author"]/a/text()').extract_first()
            comment_info['content'] = tr_comment.xpath('.//div[@class="body"]/span/text()').extract_first()
            comment_info['author_href'] = "https://www.qimai.cn" + (
                tr_comment.xpath('.//span[@class="author"]/a/@href').extract_first())
            comment_info['rate'] = tr_comment.xpath('.//input/@value').extract_first()
            comment_info['publish_time'] = tr_comment.xpath('.//td/div/span/text()').extract_first()
            comment_info['deleted'] = tr_comment.xpath('.//i[@style="display:inline-block"]/text()').extract_first()
            if self.query_type.__len__() == 0:
                comment_info['type'] = 2
            else:
                comment_info['type'] = 3
            yield comment_info
        if next_text is None and self.page_no < 2:
            self.page_no += 1
            yield SplashRequest(self.url, self.parse_comment, endpoint="execute",
                                args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url,
                                      'wait': 5})
        elif self.query_type.__len__() == 0:
            self.page_no = 2
            self.query_type = most_help
            yield SplashRequest(self.url, self.parse_comment, endpoint="execute",
                                args={'lua_source': page_no_lua % (self.query_type, int(self.page_no)), 'url': self.url,
                                      'wait': 5})
        else:
            yield self.app_info
