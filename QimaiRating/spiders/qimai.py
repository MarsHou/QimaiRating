# -*- coding: utf-8 -*-
import base64
import time

import scrapy


class QimaiSpider(scrapy.Spider):
    name = 'qimai'
    allowed_domains = ['qimai.cn']
    # start_urls = ['https://www.qimai.cn/app/comment/appid/1084660392/country/cn']
    start_urls = [
        'https://api.qimai.cn/app/appinfo?analysis=LGVzV34iOAQsJnQEfFQsFnkTSlURExhWQEBeV1AOdRBTCQZRAlJVBFBVDHESCA%3D%3D&appid=1084660392&country=cn',
        'https://api.qimai.cn/app/commentRate?analysis=LGVzV34iOAQsJnQEfFQsFnkTSlURExhUX11aXFgVZ1IVVHJAAl5VB1hUCAMEAVsjGgE%3D&appid=1084660392&country=cn',
        'https://api.qimai.cn/app/comment?analysis=LGVzV34iOAQsJnQEfFMrFHRkMEAsN3ZDfXRyXnsldAUsdXNVfSIgTywmfAV9bScbdWQoQygnfk1%2FWmIMeQtgBjgDBl5wRU5XERIWUl5UDwZXRCUXU1sDBQAABgkBVwNzQgA%3D&appid=1084660392&country=cn&sword=&sdate=2015-10-01+00:00:00&edate=2018-11-30+23:59:59'
    ]

    def __init__(self):
        params = {
            'appid': '1084660392',
            'country': 'cn'
        }
        path = '/app/appinfo'
        q = QiMai()
        params_b64 = q.params_b64(path, params)
        analysis = q.data_encrypt(params_b64)
        # string = q.data_decrypt(analysis)
        self.url = ['https://api.qimai.cn' + path + '?analysis=' + analysis + '&appid=1084660392&country=cn']

    def start_requests(self):
        for url in self.url:
            # yield SplashRequest(url, self.parse, args={'wait': 10})
            yield scrapy.Request(url)

    def parse(self, response):
        # pass
        # container = response.xpath('//div[@id="app-container"]').extract()
        # # container = Selector(div=container)
        # app_name = response.xpath('//div[@class="appname"]/text()').extract()
        # score_list = response.xpath('//div[@class="score-box"]').extract()
        # for score in score_list:
        #     div_score = Selector(text=score)
        #     score_header = div_score.xpath('.//div[@class="score-header"]/text()').extract()
        #     score_star = div_score.xpath('.//div[@class="score-star"]/p[@class="num"]/text()').extract()
        #     comment_num = div_score.xpath('.//div[@class="score-star"]/p[@class="comment-num-item"]/text()').extract()
        #     # print(score_header, score_star, comment_num)
        # td_list = response.xpath('//tbody[@class="ivu-table-tbody"]/tr/td').extract()
        print(response.body)


class QiMai(object):
    def __init__(self):
        self.string = 'a12c0fa6ab9119bc90e4ac7700796a53'

    def params_b64(self, path, params=None):
        if not params:
            t = int(time.time() * 1000) - 1515125653845
            return '@#' + path + '@#' + str(t) + '@#1'
        params_list = []
        for key in params:
            params_list.append(params[key])
        params_list.sort()
        params = ''.join(params_list)
        params_b64 = base64.b64encode(params.encode()).decode()
        t = int(time.time() * 1000) - 1515125653845
        params = params_b64 + '@#' + path + '@#' + str(t) + '@#1'
        return params

    def data_encrypt(self, data):
        # 异或运算加密
        data_list = list(data)
        for i in range(0, len(data_list)):
            data_list[i] = chr(ord(data_list[i]) ^ ord(self.string[i % len(self.string)]))
        return base64.b64encode(''.join(data_list).encode()).decode()
