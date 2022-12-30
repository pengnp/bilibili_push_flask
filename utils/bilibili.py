import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from utils.yaml_util import YamlUtil
from utils.send_email import SendEmail
from utils.config import TEMPLATES_PATH, DATA_YAML_PATH, BILI_EVENT, header
from utils.decorator import retry
from time import sleep


class BILIBILI:

    def __init__(self):
        self._demo_html = "template.html"
        self._executor = ThreadPoolExecutor(max_workers=3)
        self._yaml_fun = YamlUtil(DATA_YAML_PATH)
        self.data_result = {}

    def _template_render(self, datas, model):
        loader = FileSystemLoader(TEMPLATES_PATH)
        env = Environment(loader=loader)
        template = env.get_template(self._demo_html)
        html = template.render(data=datas, ID=model)
        return html

    @retry
    def _search_api(self, umid):
        url = 'https://api.bilibili.com/x/space/wbi/arc/search'
        param = {
            'mid': umid,
            'ps': 10,
            'tid': 0,
            'pn': 1,
            'order': 'pubdate',
            'order_avoided': 'true',
        }
        return requests.get(url=url, headers=header, params=param).json()

    def _time_diff(self, start_time):
        end_time = datetime.date(datetime.now())
        t1 = datetime.date(datetime.fromtimestamp(start_time))
        time_diff = (end_time - t1).days
        if time_diff < 0:
            print(f'now_date: {end_time}, video_date: {t1}, diff: {time_diff}')
        return time_diff

    def update_user_info(self, user_k, user_v, flag=False):
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
        followings_res = requests.get(url=url, headers=header, params=param).json()
        total = followings_res['data']['total']
        if total % 50 == 0:
            for_count = total // 50
        else:
            for_count = total // 50 + 1
        for i in range(1, for_count + 1):
            if i != 1:
                param['pn'] = i
                followings_res = requests.get(url=url, headers=header, params=param).json()
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
            BILI_EVENT.ALL_EVENT['update'] = False
            print(f'{user_k}添加完成')
        if result:
            return '有up更改了名字', user_v['email'], result

    def _analysis(self, old_data, new_data, user_k):
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
        return False

    def push(self, user_k, user_v):
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

    def week_chenck(self, user_k, user_v):
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

    def _event_check(self, event1, event2, event3):
        while BILI_EVENT.ALL_EVENT[event2] or BILI_EVENT.ALL_EVENT[event3]:
            sleep(3)
            print(f'检测到数据文件正在被使用,任务{event1}暂时停止')
        BILI_EVENT.ALL_EVENT[event1] = True

    def start(self, event, function):
        event_list = ['push', 'update', 'check']
        threading_list = []
        if event in event_list:
            event_list.remove(event)
            self._event_check(event, event_list[0], event_list[1])
            print(f'定时任务执行, 执行任务：{event}, 执行时间：{datetime.now()}')
            self.data_result = self._yaml_fun.read
            for user_k, user_v in self.data_result.items():
                if self.data_result[user_k][event] == 'Y':
                    threading_list.append(self._executor.submit(function, user_k, user_v))
            for future in as_completed(threading_list):
                f = future.result()
                if f:
                    SendEmail(f[0], f[1], f[2]).send_email()
            self._yaml_fun.write_w(self.data_result)
            BILI_EVENT.ALL_EVENT[event] = False
            print(f'定时任务执行{event}, 执行完成')
        else:
            print(f'添加用户：{event}, 执行时间：{datetime.now()}')
            BILI_EVENT.ALL_EVENT['update'] = True
            self.data_result = self._yaml_fun.read
            threading_list.append(self._executor.submit(function, event, self.data_result[event], True))
            as_completed(threading_list)


if __name__ == '__main__':
    BILI = BILIBILI()
    BILI.start('update', BILI.update_user_info)