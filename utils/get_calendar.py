from pprint import pprint
import json
import requests
from lxml import etree
import datetime
from utils.config import header
from concurrent.futures import ThreadPoolExecutor, as_completed


# 日历数据
def _get_rili_data():
    festival_dict = {}
    url = 'https://www.rili.com.cn/'
    response = requests.get(url=url, headers=header).text
    res_html = etree.HTML(response)
    element_xpath = {
        'today': "//div[@class='today']/p/text()",
        'today_24jie': "//span[@id='today_24jie']/text()",
        'today_dlleft': "//span[@id='today_dlleft']/text()",
        'today_dlright': "//span[@id='today_dlright']/text()",
        'today_week_id': "//span[@id='today_week_id']/text()",
        'today_nongli': "//span[@id='today_nongli']/text()",
        'today_yi': "//ul[@id='today_yi']/li/text()",
        'today_ji': "//ul[@id='today_ji']/li/text()",
        'festival_name': "//span[@class='txt']/a/text()",
        'festival_date': "//span[@class='time']/text()",
        'festival_djs': "//span[@class='djs']/text()",
    }
    for elem, el_xpath in element_xpath.items():
        festival_dict[elem] = res_html.xpath(el_xpath)
    festival_dict['day'] = datetime.datetime.now().strftime('%d')
    return 'rili', None, festival_dict


# 新闻
def _get_news(key, value):
    url = f'https://3g.163.com/touch/reconstruct/article/list/{value}/0-10.html'
    response = json.loads(requests.get(url=url, headers=header).text[9:-1])[value]
    for data in response:
        if key in ['军事', '时尚'] and 'skipType' in data and 'photosetID' in data:
            phot_id = data['photosetID'].split('|')
            data['skipURL'] = f'https://3g.163.com/war/photoview/{phot_id[0]}/{phot_id[1]}.html'
        if data['imgsrc'] == '':
            data['imgsrc'] = '/static/img/1.jpg'
        if data['url'] == '':
            data['url'] = f"https://3g.163.com/news/article/{data['docid']}.html"
    return key, value, response


# 微博
def _get_weibo_hotnews():
    url = 'https://m.weibo.cn/api/container/getIndex'
    param = {
        "containerid": "106003type=25&t=3&disable_hot=1&filter_type=realtimehot",
        "title": "微博热搜",
        "show_cache_when_error": 1,
        "extparam": "seat=1&lcate=1001&pos=0_0&dgr=0&filter_type=realtimehot&mi_cid=100103&region_relas_conf=0&cate=10103&c_type=30&display_time=1672370114&pre_seqid=1044138437",
        "luicode": 10000011,
        "lfid": 231583,
    }
    response = requests.post(url, headers=header, params=param).json()['data']['cards'][0]['card_group']
    return '微博热搜', None, response


def get_data():
    executor = ThreadPoolExecutor()
    data_dict = {
        '新闻': 'BBM54PGAwangning',
        '娱乐': 'BA10TA81wangning',
        '体育': 'BA8E6OEOwangning',
        '财经': 'BA8EE5GMwangning',
        '军事': 'BAI67OGGwangning',
        '科技': 'BA8D4A3Rwangning',
        '手机': 'BAI6I0O5wangning',
        '数码': 'BAI6JOD9wangning',
        '时尚': 'BA8F6ICNwangning',
        '游戏': 'BAI6RHDKwangning',
        '教育': 'BA8FF5PRwangning',
        '健康': 'BDC4QSV3wangning',
        '旅游': 'BEO4GINLwangning',
        '微博热搜': _get_weibo_hotnews,
        'rili': _get_rili_data,  # 日历
    }
    threading_list = []
    for key, value in data_dict.items():
        if key in ['微博热搜', 'rili']:
            threading_list.append(executor.submit(value))
        else:
            threading_list.append(executor.submit(_get_news, key, value))
    for future in as_completed(threading_list):
        f = future.result()
        data_dict[f[0]] = f[2]
    return data_dict


if __name__ == '__main__':
    pprint(get_data())