# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

from idna import unicode

STYLE = r"""<style type="text/css">
table.app_info {
        margin: 0 auto;
        color: #888888;
    }

    .star {
        margin: 0 auto;
        color: #888888;
        width: 50%;
        font-size: 14px;
    }

    .header {
        color: #333333;
    }

    .score {
        color: #fe7224;
        font-size: 18px;
        padding-right: 20px;
    }

    table.app_info td {
        padding: 10px;
        color: #666666;
    }

    table.hover_table {
        margin-top: 20px;
        font-family: verdana, arial, sans-serif;
        font-size: 12px;
        color: #666666;
        border: 1px #d6d6d6;
        border-collapse: collapse;
        width: 100%;
    }

    table.hover_table th {
        background-color: #f7f7fa;
        padding: 8px;
        border: 1px solid #d6d6d6;
    }

    table.hover_table tr {
        background-color: #ffffff;
    }

    table.hover_table td {
        padding: 8px;
        border: 1px solid #d6d6d6;
    }

    .title {
        font-size: 14px;
        color: #333333;
    }

    .author {
        font-size: 12px;
        color: #666666;
    }

    a {
        color: #fe7224;
    }

    i {
        color: #faba4a;
        font-size: 12px;
    }

    h3 {
        text-align: center;
        margin-top: 20px;
    }
</style>"""


class QimairatingPipeline(object):
    all_data = {"rate_list": [], "recent_data": [], "help_data": [], "app_info": {}}

    def process_item(self, item, spider):
        data_type = item['type']
        if data_type == 1:
            rate_list = self.all_data['rate_list']
            rate_list.append(item)
            self.all_data['rate_list'] = rate_list
        elif data_type == 2:
            recent_data = self.all_data['recent_data']
            recent_data.append(item)
            self.all_data['recent_data'] = recent_data
        elif data_type == 3:
            help_data = self.all_data['help_data']
            help_data.append(item)
            self.all_data['help_data'] = help_data
        elif data_type == 0:
            self.all_data['app_info'] = item
            self.save_data()

        return item

    def save_data(self):
        app_info = self.all_data['app_info']
        rate_list = self.all_data['rate_list']
        recent_data = self.all_data['recent_data']
        help_data = self.all_data['help_data']
        file_name = 'give_rating_%s.html' % (time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        file_out = open(file_name, 'w')
        file_out.write(r'''<meta http-equiv=Content-Type content="text/html;charset=utf-8">
                <html>
                %s
                <body>
                ''' % STYLE)
        file_out.write((r'''
        <h3>%s</h3>
        ''' % app_info['app_name']).encode('utf-8'))
        file_out.write(unicode(r'''
        <div>
    <table class="app_info">
        <tr>
            <th>AUTHOR</th>
            <th>APP ID</th>
            <th>PRICE</th>
            <th>LAST VERSION</th>
        </tr>
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
    </table>
</div>
<div class="star">
        ''' % (app_info['app_author'], app_info['app_id'], app_info['app_price'], app_info['app_last_version'])).encode(
            'utf-8'))
        for rate in rate_list:
            file_out.write(unicode(r'''
            <span class="header">%s</span>
    <span class="score">%s</span>
    <span class="score_num">%s</span>
    <br/>
            ''' % (rate['score_header'], rate['score_star'], rate['comment_num'])).encode('utf-8'))
        file_out.write(r'''
        </div>
<h4>MOST RECENT</h4>
<table class='hover_table'>
    <tr>
        <th>NO</th>
        <th>CONTENT</th>
        <th>TIME</th>
        <th>RATING</th>
    </tr>
        ''')
        no = 1
        for data in recent_data:
            file_out.write(self.get_tr_content(data, no))
            no += 1
        file_out.write(r'''
        </table><br>
        ''')
        file_out.write(r'''
        <h4>MOST HELP</h4>
        <table class='hover_table'>
            <tr>
                <th>NO</th>
                <th>CONTENT</th>
                <th>TIME</th>
                <th>RATING</th>
            </tr>
                ''')
        no = 1
        for data in help_data:
            file_out.write(self.get_tr_content(data, no))
            no += 1
        file_out.write(r'''
                </table><br></body>
        </html>
                ''')
        file_out.close()
        return file_name

    def get_tr_content(self, data, no):
        return unicode(r"""<tr onmouseover="this.style.backgroundColor='#ebf7ff';"
        onmouseout="this.style.backgroundColor='#ffffff';">
        <td>%s</td>
        <td>
            <div>
                <p class="title"><span>%s</span><span class="author">作者：<a
                        href="%s">%s</a></span>
                    <i>%s</i>
                </p>
                <div class="body">
                    <span>%s</span>
                </div>
            </div>
        </td>
        <td>%s</td>
        <td>%s</td>
    </tr>""" % (
            no, data['title'], data['author_href'], data['author'], data['deleted'], data['content'],
            data['publish_time'],
            data['rate'])).encode('utf-8')
