import requests
from lxml import etree
import datetime


def get_data():
    festival_dict = {}
    url = 'https://www.rili.com.cn/'
    header = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/107.0.0.0"
    }
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
    return festival_dict
