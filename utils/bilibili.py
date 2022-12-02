import requests
from time import sleep
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from utils.yaml_util import YamlUtil
from utils.send_email import SendEmail
from utils.config import TEMPLATES_PATH, DATA_YAML_PATH


class PushAndUpdate:

    def __init__(self):
        self._demo_html = "template.html"
        self._executor = ThreadPoolExecutor(max_workers=3)
        self._header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/107.0.0.0"
        }
        self._yaml_fun = YamlUtil(DATA_YAML_PATH)

    def _template_render(self, datas, model):
        """
        :param datas: 需要推送的视频数据
        :param model: 设备型号 Android、ios
        :return: 写入好的数据模板
        """
        loader = FileSystemLoader(TEMPLATES_PATH)
        env = Environment(loader=loader)
        template = env.get_template(self._demo_html)
        html = template.render(data=datas, ID=model)
        return html

    def _search_api(self, umid):
        """
        获取up视频数据
        :param umid: up的id
        :return: 返回接口数据
        """
        sleep(random.uniform(1.0, 3.0))
        url = 'https://api.bilibili.com/x/space/arc/search'
        param = {
            'mid': umid,
            'ps': 10,
            'tid': 0,
            'pn': 1,
            'order': 'pubdate',
            'jsonp': 'jsonp'
        }
        response = requests.get(url=url, headers=self._header, params=param).json()
        if response['code'] == 0:
            return response
        else:
            print(f'{umid}请求有误, 接口返回：{response}')
            return None

    def _time_diff(self, start_time, end_time=datetime.now()):
        """
        计算两个时间差，单位 day
        """
        t1 = datetime.fromtimestamp(start_time)
        time_diff = (end_time - t1).days
        return time_diff

    def _update_user_info(self, user_k, user_v, flag=False):
        """
        更新本地user数据
        :param user_k: user的名称
        :param user_v: user数据
        :return: False
        """
        new_user_data = {}
        url = 'https://api.bilibili.com/x/relation/followings'
        param = {
                'vmid': user_v['mid'],
                'pn': 1,
                'ps': 50,
                'order': 'desc',
                'order_type': 'attention',
                'jsonp': 'jsonp'
        }
        followings_res = requests.get(url=url, headers=self._header, params=param).json()
        total = followings_res['data']['total']
        if total % 50 == 0:
            for_count = total // 50
        else:
            for_count = total // 50 + 1
        for i in range(1, for_count + 1):
            if i != 1:
                param['pn'] = i
                followings_res = requests.get(url=url, headers=self._header, params=param).json()
            for data in followings_res['data']['list']:
                umid, name = data['mid'], data['uname']
                response = self._search_api(umid)
                if response is not None:
                    video_count = response['data']['page']['count']
                    video_datas = response['data']['list']['vlist']
                    if video_count < 20:
                        continue
                    time_diff = self._time_diff(video_datas[0]['created'])
                    new_user_data[umid] = [name, video_count, time_diff]
        result = self._analysis(user_v['mids'], new_user_data, user_k)
        if flag:
            self._yaml_fun.write_w(self.data_result)
            print(f'{user_k}添加完成')
        if result:
            return '有up更改了名字', user_v['email'], result

    def _analysis(self, old_data, new_data, user_k):
        """
        与本地数据进行对照处理
        :param old_data: 本地user数据
        :param new_data: 新的user数据
        :param user_k: user的名称
        :return:
        """
        history = {'添加': [], '删除': [], '更改名字': []}
        differ = old_data.keys() ^ new_data.keys()
        same = old_data.keys() & new_data.keys()
        if same:
            for umid in same:
                self.data_result[user_k]['mids'][umid][2] = new_data[umid][2]
        if differ:
            for umid in differ:
                if umid not in new_data:
                    history['删除'].append(old_data[umid][0])
                    del self.data_result[user_k]['mids'][umid]
                    continue
                if umid not in old_data:
                    history['添加'].append(new_data[umid][0])
                    self.data_result[user_k]['mids'][umid] = new_data[umid]
        else:
            for umid, uv in new_data.items():
                if uv[0] != old_data[umid][0]:
                    history['更改名字'].append(f'{old_data[umid][0]} --> {uv[0]}')
                    self.data_result[user_k]['mids'][umid][0] = uv[0]
        print(user_k)
        for k, v in history.items():
            if v:
                print(f'\t {k}: {v}')
                if k == '更改名字':
                    return f"<p style='font-size:15px;'> {v} </p>"
        return None

    def _push(self, user_k, user_v):
        """
        推送检测
        :param user_k: user名称
        :param user_v: user数据
        :return: 有更新返回发邮件所需数据，无则返回False
        """
        push_datas = {}
        for umid, uv in user_v['mids'].items():
            if uv[2] > 7:
                continue
            response = self._search_api(umid)
            if response is not None:
                video_count = response['data']['page']['count']
                video_datas = response['data']['list']['vlist']
                if video_count > uv[1]:
                    data_list = []
                    for video in video_datas[:video_count - uv[1]]:
                        pic = video['pic']
                        title = video['title']
                        bvid = video['bvid']
                        length = video['length']
                        if len(title) > 80:
                            title = title[:80] + '...'
                        data_list.append([pic, title, bvid, length])
                    push_datas[uv[0]] = data_list
                    self.data_result[user_k]['mids'][umid][1] = video_count
        if push_datas:
            unames = list(push_datas.keys())
            print(f'{user_k}: {unames}')
            if len(unames) > 4:
                subject = f"{'、'.join(unames[:4]) + '...'}等{len(unames)}位up更新了视频"
            else:
                subject = f"{'、'.join(unames)}更新了视频"
            msg = self._template_render(push_datas, user_v['model'])
            return subject, user_v['email'], msg
        return False

    def _week_chenck(self, user_k, user_v):
        """
        鸽子检查
        :param user_k: user名称
        :param user_v: user数据
        :return: 有鸽子返回发邮件所需数据，无则返回False
        """
        msg = ''
        subject = '本星期鸽子总结'
        print(user_k)
        for up_v in user_v['mids'].values():
            if up_v[2] >= 7:
                print(f'\t {up_v[0]}已经鸽了{up_v[2]}天')
                msg += f'''
                    <p style="font-size:15px;">
                        <span style="font-weight:bold;">【 {up_v[0]} 】</span> 已经鸽了 <span style="font-weight:bold;">【 {up_v[2]} 】</span> 天未更新视频
                    </p>\n
                '''
        if msg:
            return subject, user_v['email'], msg
        return False

    def start(self, config_key):
        """
        梦开始的地方
        :param config_key: configure.yml中的key，根据相应的key执行相应的动作
        :return:
        """
        self.data_result = self._yaml_fun.read
        threading_list = []
        if config_key not in ['push', 'update', 'check']:
            print(f'添加用户{config_key}, 执行时间：{datetime.now()}')
            import threading
            th = threading.Thread(target=self._update_user_info, args=(config_key, self.data_result[config_key], True))
            th.daemon = True
            th.start()
        else:
            print(f'定时任务执行, 执行任务：{config_key}, 执行时间：{datetime.now()}')
            for user_k, user_v in self.data_result.items():
                if self.data_result[user_k]['push'] == 'Y' and config_key == 'push':
                    threading_list.append(self._executor.submit(self._push, user_k, user_v))
                elif self.data_result[user_k]['update'] == 'Y' and config_key == 'update':
                    threading_list.append(self._executor.submit(self._update_user_info, user_k, user_v))
                elif self.data_result[user_k]['check'] == 'Y' and config_key == 'check':
                    threading_list.append(self._executor.submit(self._week_chenck, user_k, user_v))
        for future in as_completed(threading_list):
            f = future.result()
            if f:
                SendEmail(f[0], f[1], f[2]).send_email()
        if config_key in ['push', 'update']:
            self._yaml_fun.write_w(self.data_result)


if __name__ == '__main__':
    PushAndUpdate().start('push')