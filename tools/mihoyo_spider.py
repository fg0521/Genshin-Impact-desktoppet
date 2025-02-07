import copy
import json
import os
import pprint
import re
import time
import pandas as pd
import requests
# -*- coding:utf-8 -*-
# coding=gb2312



false = null = true = ''


class MiHoYoSpider():

    def __init__(self):
        self.url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id='
        self.path = 'your save path'
        self.id = 'id list for spider'

    def parse(self):
        """
        code for parsing html
        need to rewrite it
        """
        pass

    def clear(self):
        """
        code for clearing csv file
        need to rewrite it
        """
        pass


class CharacterSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.char_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/character-id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-character.csv'

    def parse(self):
        for i in self.char_id:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                res = eval(res.text)
                data = eval(str(res['data']['content']).replace('\\n', ''))
                # pprint.pprint(data)
                role_name = data['title']
                info = eval(data['ext'])["c_25"]["filter"]["text"]
                icon = data['icon']
                summary = data['summary']
                html1 = data['contents'][0]['text']
                shown = data['contents'][2]['text']
                # pprint.pprint(shown)
                txt = [re.sub('<(.*?)>', '', str(i)) for i in
                       re.findall('style="white-space: pre-wrap;">(.*?)</p><p ', shown)]
                with open('../rec_intention/yuanshen.txt', 'a+') as f:
                    [f.write(i + '\n') for i in txt]
                # pprint.pprint(txt)
                # break
                # introduce = re.findall('class="obc-tmp-character__value">(.*?)</div></div>', html1)
                # broken = re.findall(
                #     'class="obc-tmpl__icon-text">([\u4e00-\u9fa5]+)</span></a> <span class="obc-tmpl__icon-num">(\*[\d]+)</span>',
                #     html1)
                # desc = re.findall('pre-wrap;">(.*?)</p></td>', html1)
                # attr = re.findall('pre-wrap; text-align: center;">(.*?)</p>', html1)
                # weapons = re.findall(
                #     'alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">([\u4e00-\u9fa5]+)</span></a> <!----></div></td>',
                #     html1)
                # html2 = data['contents'][1]['text']
                # attack = re.findall('class="obc-tmpl__icon-text">(.*?)</span> ', html2)
                # skill_desc = re.findall('obc-tmpl__pre-text">(.*?)</pre>', html2)
                # live_desc = re.findall('<td>(.*?)</td></tr><tr><td><div', html2)
                # skill_book = re.findall(
                #     '<span class="obc-tmpl__icon-text">([\u4e00-\u9fa5「」]+)</span></a> <span class="obc-tmpl__icon-num">(\*[\d]+)</span></div></div><div>',
                #     html2)
                # mz_desc = [i for i in attack if 'span' not in i and 'class' not in i]
                # mz_effect = [i for i in live_desc if 'span' not in i and 'class' not in i]
                # print(f'{i}:{role_name}')
                # df = pd.DataFrame(data=[{'编号': i, '名字': role_name, '介绍': info, '图片': icon, '总结': summary,
                #                          '信息': introduce, '突破材料': broken, '武器选择': desc, '圣遗物': attr, '武器': weapons,
                #                          'skill_book': skill_book, '命座描述': mz_desc, '技能描述': skill_desc,
                #                          '命座': mz_effect}])
                #
                # if os.path.exists(self.path):
                #     df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                # else:
                #     df.to_csv(self.path, index=False, encoding='utf-8')
                time.sleep(2)

    def clear(self):
        pass


class MasterSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.master_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/master-id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-master.csv'

    def parse(self):
        for i in self.master_id:
            url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id=' + str(
                i)
            res = requests.get(url)
            if res.status_code == 200:
                html = eval(res.text.replace('\\n', ''))
                # pprint.pprint(html)
                contents = html['data']['content']['contents'][0]['text']
                name = html['data']['content']['title']
                id = html['data']['content']['id']
                dropping = [i for i in re.findall('<p class="obc-tmpl__material-name">(.*?)</p> ', contents) if
                            len(i) < 50]
                attack = [i for i in re.findall('pre-wrap;">(.*?)</p></td></tr><tr><td ', contents) if len(i) < 50]
                element = [i for i in re.findall('style="">(.*?)</p></td></tr><tr><td ', contents) if len(i) < 50]
                method = [i for i in re.findall('<li><p style="white-space: pre-wrap;">(.*?)</p></li>', contents) if
                          len(i) < 50]
                backstory = [i for i in re.findall('pre-wrap;">(.*?)</p>', contents) if
                             i not in method and i not in attack and '注：' not in i]
                print(id, name)
                df = pd.DataFrame(
                    data=[{'id': id, 'name': name, 'dropping': dropping, 'attack': attack, 'element': element,
                           'method': method, 'backstory': backstory}])
                if os.path.exists('../rec_intention/kg_data/master2.csv'):
                    df.to_csv('../rec_intention/kg_data/master2.csv', mode='a', index=False, header=False,
                              encoding='utf-8')
                else:
                    df.to_csv('../rec_intention/kg_data/master2.csv', index=False, encoding='utf-8')
            time.sleep(2)

    def clear(self):
        df = pd.read_csv('../rec_intention/kg_data/master.csv')

        def get_ele(attack):
            attack = eval(attack)
            e, a = '无', []
            if attack:
                if attack[0] in ['无', '风', '火', '水', '岩', '雷', '冰', '物理', '草']:
                    e = attack[0]
                attack.remove(attack[0])
                a = attack
            return e

        df['element'] = df.apply(lambda x: get_ele(x['attack']), axis=1)
        df['attack'] = df['attack'].apply(
            lambda x: str([i for i in eval(x) if i not in ['无', '风', '火', '水', '岩', '雷', '冰', '物理', '草']]))

        df.to_csv('../rec_intention/kg_data/done/label-master.csv', index=False, encoding='utf-8')
        print(df[['element', 'attack']])


class FoodSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.food_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/food-id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-food.csv'

    def parse(self):
        for i in [2455, 2567, 2607, 2762, 2763, 2764, 2765, 2766, 2767, 2768, 2769, 2770, 2771, 2772, 2775, 2824, 2854,
                  2855, 2873, 2876, 3051, 3052, 3053, 3054, 3055, 3056, 3057, 3058, 3059, 3060, 3061, 3062, 3164, 3165,
                  3166, 3379, 3426, 3530, 3567, 3577, 3654, 3865, 3914, 3964, 4338, 4339, 4387, 4388, 4389, 4390, 4538,
                  4539, 4608, 4635, 4636, 4637, 4638, 4639, 4640, 4755, 4863, 4893, 4894, 4895, 4896, 4897, 4898]:
            try:
                foods = []
                url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id=' + str(
                    i)
                res = requests.get(url)
                if res.status_code == 200:
                    data = eval(res.text)['data']['content']
                    try:
                        food_desc = eval(data['ext'])['c_21']['filter']['text']

                    except:
                        food_desc = []
                    text = data['contents'][0]['text']
                    # pprint.pprint(data)
                    name = re.findall('名称：(.*?)<', text)

                    try:
                        material = re.findall('class="obc-tmpl__icon-text">([\u4e00-\u9fa5]+)</span></a> <span ', text)
                        num = re.findall('class="obc-tmpl__icon-num">(\*\d+)</span></div>', text)
                    except:
                        material, num = [], []
                    descs = re.findall('描述：(.*?)<', text)
                    effect = re.findall('使用效果：(.*?)<', text)
                    get_method = re.findall('获得方式：(.*?)<', text)
                    food_map = re.findall('食谱获得：(.*?)</p>', text)
                    print(i, name)
                    # print(name,material,num,descs,effect,get_method,food_map)
                    # foods.append(
                    #     {'food_id': i, 'info': food_desc, 'name': name, 'material': material, 'num': num,'descs':descs,
                    #                        'effect':effect,'method':get_method,'get':food_map})
                    mat_num = list(set([material[i] + num[i] for i in range(len(num))]))
                    for k in range(len(name)):
                        foods.append({'food_id': i, 'info': food_desc, 'name': name[k], 'material': str(mat_num),
                                      'desc': descs[k],
                                      'effect': effect[k], 'method': get_method[k], 'get': food_map[k]})

                    df = pd.DataFrame(foods)
                    if os.path.exists('../rec_intention/kg_data/food.csv'):
                        df.to_csv('../rec_intention/kg_data/food.csv', mode='a', index=False, header=False,
                                  encoding='utf-8')
                    else:
                        df.to_csv('../rec_intention/kg_data/food.csv', index=False, encoding='utf-8')

            except Exception as e:
                print(i)
                continue
            time.sleep(2)

    def clear(self):
        df = pd.read_csv('../rec_intention/kg_data/food.csv')
        df['info'] = df['info'].apply(lambda x: '|'.join([i.split('/')[1] for i in sorted(eval(x))]))
        df1 = df['info'].str.split('|', expand=True)
        df.drop(['info'], inplace=True, axis=1)
        df1.columns = ['func_type', 'rarity', 'getting1']
        # print(df1)
        df = df.join(df1)

        def fill_food_name(name, cond):
            name, cond = str(name), str(cond)
            # print(cond)
            if name != 'nan':
                s = name
            else:
                if cond.startswith('完成烹饪'):
                    s = '奇怪的' + cond[4:]
                elif cond.startswith('成功烹饪'):
                    s = cond[4:]
                elif cond.startswith('完美烹饪'):
                    s = '美味的' + cond[4:]
                else:
                    s = 'None'
            return s

        df['name'] = df.apply(lambda x: fill_food_name(x['name'], x['condition']), axis=1)
        df['getting'] = df.apply(lambda x: '【' + str(x['getting1']) + '】' + str(x['getting']), axis=1)
        df.drop(['getting1'], axis=1, inplace=True)
        df.insert(0, 'id', [i for i in range(1, len(df) + 1)])
        df.to_csv('../rec_intention/kg_data/done/label-food.csv', index=False, encoding='utf-8')
        print(df)


class WeaponSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.weapon_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/weapon_id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-weapon.csv'

    def parse(self):
        for i in self.weapon_id:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                # pprint.pprint(eval(res.text))
                data = eval(res.text)['data']['content']
                name = data['title']
                id = data['id']
                icon = data['icon']
                ext = eval(eval(data['ext'])["c_5"]["filter"]["text"])
                text = data['contents'][0]['text'].replace('\n', '')
                desc = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('装备描述(.*?)冒险等阶限制', text)]
                limit = re.findall('obc-tmpl__rich-text">冒险等阶限制：(.*?)</td></tr>', text)
                # getting = [re.sub('<(.*?)>','',str(i)) for i in re.findall('obc-tmpl__rich-text">获取途径：(.*?)</p></td></tr>',text)]
                story = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('相关故事(.*?)</p></div>', text)]
                material = [re.sub('<(.*?)>', '', str(i)) for i in
                            re.findall('<span class="obc-tmpl__icon-text">(.*?)</span>', text)]
                material_num = [re.sub('<(.*?)>', '', str(i)) for i in
                                re.findall('<span class="obc-tmpl__icon-num">(.*?)</span>', text)]
                grade = [re.sub('<(.*?)>', '', str(i)) for i in
                         re.findall('class="obc-tmpl__switch-btn">(.*?)</li>', text)]
                effect = [re.sub('<(.*?)>', '', str(i)) for i in
                          re.findall('<tbody><tr><td colspan="\d">(.*?)</li></ul></td></tr></tbody>', text)]
                print(name)
                data = [{'name': name, 'id': id, 'ext': ext, 'desc': desc, 'limit': limit, 'story': story,
                         'material': material, "material_num": material_num, 'grade': grade, 'effect': effect,
                         'icon': icon}]
                df = pd.DataFrame(data=data)
                if os.path.exists(self.path):
                    df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                else:
                    df.to_csv(self.path, index=False, encoding='utf-8')
                time.sleep(2)

    def clear(self):
        # name,id,ext,desc,limit,getting,story,material,"material_num",grade,effect
        df = pd.read_csv(self.path)

        def split_ext(x):
            x = eval(x)
            res = {'武器类型': 'None', '武器星级': 'None', '属性加成': 'None', '获取途径': 'None'}
            for i in x:
                s = i.split('/')
                if res[s[0]] != 'None':
                    res[s[0]] = res[s[0]] + f"、{s[1]}"
                else:
                    res[s[0]] = s[1]
            res = [v for _, v in res.items()]
            return '|'.join(res)

        df['ext'] = df['ext'].apply(lambda x: split_ext(x))
        df1 = df['ext'].str.split('|', expand=True)
        df1.columns = ['weapon_type', 'rarity', 'attr_add', 'getting']
        df = df.join(df1)

        def skill(x, mode=0):
            x = eval(x)
            if not x:
                return 'None'
            else:
                if mode == 0:
                    s = ''.join(re.findall('\)(.*?)·', x[0]))
                    return s if s else 'None'
                else:
                    sp = ''.join(re.findall('\)(.*?)·', x[0])) + '·'
                    return x[0].replace(sp, '')

        df['introd'] = df['desc'].apply(lambda x: skill(x, 0))
        df['refine'] = df['desc'].apply(lambda x: skill(x, 1))

        def add_material_num(name, num):
            name, num = eval(name), eval(num)
            index = name.index('摩拉')
            res = []
            for i in range(index):
                res.append(name[i] + num[i])
            return str(res)

        df['material'] = df.apply(lambda x: add_material_num(x['material'], x['material_num']), axis=1)
        df['grade'] = df['grade'].apply(lambda x: [i.replace(' ', '') for i in eval(x) if '角色' not in i])

        def add_breaking(grade, effect):
            grade, effect = grade, eval(effect)
            res = {}
            for i in range(len(grade)):
                g = grade[i]
                e = effect[i]
                res[g] = e
            return str(res)

        df['breaking'] = df.apply(lambda x: add_breaking(x['grade'], x['effect']), axis=1)
        df = df[['name', 'id', 'limit', 'story', 'material', 'icon', 'breaking', 'introd', 'refine', 'weapon_type',
                 'rarity', 'attr_add', 'getting']]
        df['limit'] = df['limit'].apply(lambda x: eval(x)[0] if eval(x) else '无')
        df['story'] = df['story'].apply(lambda x: ''.join(eval(x)))
        df['label'] = 'weapon'
        print(df.head(10))
        df.to_csv('../rec_intention/kg_data/done/label-weapon.csv', index=False, encoding='utf-8')


class NPCSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.npc = list(pd.read_csv('../rec_intention/kg_data/mhy-id/npc_id.csv')['id'])
        self.path = '../rec_intention/kg_data/to_do/label-npc.csv'

    def parse(self):
        for i in self.npc:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                data = eval(res.text)['data']['content']
                name = data['title']
                id = data['id']
                icon = data['icon']
                text = data['contents'][0]['text'].replace('\n', '')
                sex = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('<td class="h3">性别</td> <td>(.*?)</td>', text)]
                sex = sex[0] if sex else ''
                pos = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('<td class="h3">位置</td> <td>(.*?)</td>', text)]
                pos = pos[0] if pos else ''
                task = [re.sub('<(.*?)>', '', str(i)) for i in
                        re.findall('<td class="h3">相关任务</td> <td>(.*?)</td>', text)]
                task = task[0] if task else ''
                profession = [re.sub('<(.*?)>', '', str(i)) for i in
                              re.findall('class="obc-tmpl__rich-text"><p>(.*?)</p></td></tr>', text)]
                profession = profession[0] if profession else ''
                tips = [re.sub('<(.*?)>', '', str(i)) for i in
                        re.findall('<p style="white-space: pre-wrap;">(.*?)</p></td></tr>', text)]
                tips = list(set(tips))
                print(id, name)
                df = pd.DataFrame(data=[
                    {'nhy_id': id, 'name': name, 'sex': sex, 'pos': pos, 'task': task, 'profession': profession,
                     'tips': tips, 'icon': icon}])
                # pprint.pprint(data)
                if os.path.exists(self.path):
                    df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                else:
                    df.to_csv(self.path, index=False, encoding='utf-8')
                time.sleep(2)

    def clear(self):
        df = pd.read_csv(self.path)
        df['task'] = df['task'].apply(lambda x: '暂无' if x in ['无', '暂无数据', '待录入'] else x)
        df['profession'] = df['profession'].apply(lambda x: '暂无' if x in ['无', '暂无数据', '待录入'] else x)
        df['tips'] = df['tips'].apply(
            lambda x: str([i for i in eval(x) if not re.findall('\[每(.*?)日\]|食谱：|\[每周\]| \* |\d', i)]))
        df['tips'] = df['tips'].apply(lambda x: ''.join(eval(x)))
        df.fillna('暂无', inplace=True, axis=1)
        df.to_csv('../rec_intention/kg_data/done/label-npc.csv', index=False, encoding='utf-8')
        print(df['tips'])


class BreakMaterialSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()

    def clear(self):
        df = pd.read_csv('../rec_intention/kg_data/breaking_material.csv')
        df = df[['material_id', 'name', 'info']]

        def split_info(x, mode):
            x = (eval(x))
            x = [re.sub('[\d]+级\*(\d\d|\d)[；]*', '', i) for i in x]
            getting_idx, desc_idx, using_idx = -1, -1, -1
            for i in range(len(x)):
                # if '获得方式：' in x[i]:
                #     getting_idx = i
                if x[i].startswith('描述：'):
                    desc_idx = i
                if x[i].startswith('用途：'):
                    using_idx = i
            if mode == 1:
                return ''.join(x[:desc_idx])
            if mode == 2:
                return ''.join(x[desc_idx + 1:using_idx])
            if mode == 3:
                return ''.join(x[using_idx + 1:])

        df['getting'] = df['info'].apply(lambda x: split_info(x, 1))
        df['desc'] = df['info'].apply(lambda x: split_info(x, 2))
        df['using'] = df['info'].apply(lambda x: split_info(x, 3))
        df.drop(['info'], axis=1, inplace=True)
        print(df.head(10))
        df.to_csv('../rec_intention/kg_data/breaking_material1.csv', index=False, encoding='utf-8')


class AreaSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.area_id = list(set(list(pd.read_csv('../rec_intention/kg_data/mhy-id/area-id.csv')['mhy_id'])))
        self.path = '../rec_intention/kg_data/to_do/label-area.csv'

    def parse(self):
        # print(self.area_id)
        a = [1413, 115, 247, 120, 121]
        for i in a:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                try:
                    data = eval(res.text)['data']['content']
                    # pprint.pprint(data)
                    id = data['id']
                    icon = data['icon']
                    name = data['title']
                    print(id, name, 'get')
                    try:
                        text = data['contents'][0]['text']
                    except:
                        text = data['content']

                    desc = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('简述</td> <td>(.*?)</td>', text)]
                    decryption = [re.sub('<(.*?)>', '|', str(i)) for i in
                                  re.findall('<h2>机关</h2> (.*?)</tbody></table>', text)]
                    evil_task = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('魔神任务</td> <td>(.*?)</td>', text)]
                    legend_task = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('传说任务</td> <td>(.*?)</td>', text)]
                    delegate_task = [re.sub('<(.*?)>', '|', str(i)) for i in
                                     re.findall('委托任务</td> <td>(.*?)</td>', text)]
                    world_task = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('世界任务</td> <td>(.*?)</td>', text)]
                    common_master = [re.sub('<(.*?)>', '|', str(i)) for i in
                                     re.findall('普通怪物</td> <td>(.*?)</td>', text)]
                    elite_master = [re.sub('<(.*?)>', '|', str(i)) for i in
                                    re.findall('精英怪物</td> <td>(.*?)</td>', text)]
                    boss_master = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('BOSS</td> <td>(.*?)</td>', text)]

                    role_material = [re.sub('<(.*?)>', '|', str(i)) for i in
                                     re.findall('角色养成素材</td> <td>(.*?)</td>', text)]
                    ingredient = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('食材</td> <td>(.*?)</td>', text)]
                    material = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('材料</td> <td>(.*?)</td>', text)]
                    specialty = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('区域特产</td> <td>(.*?)</td>', text)]

                    # pprint.pprint(data)
                    df = pd.DataFrame(
                        data=[{'mhy_id': id, 'name': name, 'desc': str(desc), 'decryption': str(decryption),
                               'evil_task': str(evil_task),
                               'legend_task': str(legend_task), 'delegate_task': str(delegate_task),
                               'world_task': str(world_task),
                               'common_master': str(common_master), 'elite_master': str(elite_master),
                               'boss_master': str(boss_master),
                               'role_material': str(role_material), 'ingredient': str(ingredient),
                               'material': str(material), 'specialty': str(specialty),
                               'icon': icon}])
                    if os.path.exists(self.path):
                        df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                    else:
                        df.to_csv(self.path, index=False, encoding='utf-8')
                except:
                    print(id, name, 'error')
                    continue
            time.sleep(2)
            # break

    def clear(self):
        df = pd.read_csv(self.path)
        # df['sec_area'] = df['desc'].apply(lambda x:)
        for col in list(df.columns)[3:-1]:
            df[col] = df[col].apply(lambda x: [i for i in eval(x)[0].split('|') if
                                               i.replace(' ', '').replace('非战斗类', '').replace('战斗类', '')] if eval(
                x) else '暂无')
        # print(df['delegate_task'])
        # df1 = pd.read_csv('../rec_intention/kg_data/mhy-id/area-id.csv')
        # area_dic = {}
        # for _,row in df1.iterrows():
        #     area_dic[row['first_area']] = {'second_area':row['second_area'],'country':row['country']}
        # df['sec_area'] = ''
        # df['country'] = ''
        # for idx,row in df.iterrows():
        #     df.loc[idx,'sec_area'] = area_dic[row['name']]['second_area']
        #     df.loc[idx,'country'] = area_dic[row['name']]['country']
        df.to_csv('../rec_intention/kg_data/done/label-area.csv', index=False, encoding='utf-8')


class MaterialSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.material_id = list(set(list(pd.read_csv('../rec_intention/kg_data/add_material.csv')['mhy_id'])))
        self.path = '../rec_intention/kg_data/to_do/label-material2.csv'

    def parse(self):
        for i in self.material_id:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                try:
                    data = eval(res.text)['data']['content']
                    # pprint.pprint(data)

                    id = data['id']
                    icon = data['icon']
                    name = data['title']
                    print(id, name, 'get')
                    try:
                        text = data['contents'][0]['text']
                    except:
                        text = data['content']

                    getting = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('获得方式：</label>(.*?)</td>', text)]
                    description = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('描述：(.*?)</p></td>', text)]
                    using = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('用途：(.*?)</p></td>', text)]

                    # pprint.pprint(data)
                    # mhy_id,name,type,getting,description,using,label
                    df = pd.DataFrame(
                        data=[{'mhy_id': id, 'name': name, 'type': 'cooking', 'description': str(description),
                               'getting': str(getting), 'using': str(using),
                               'icon': icon, 'label': 'material'}])
                    if os.path.exists(self.path):
                        df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                    else:
                        df.to_csv(self.path, index=False, encoding='utf-8')
                except:
                    # print(id, name, 'error')
                    continue
            time.sleep(2)
            # break


class InstanceSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.instance_id = list(set(list(pd.read_csv('../rec_intention/kg_data/instance.csv')['mhy_id'])))
        self.path = '../rec_intention/kg_data/to_do/label-instance.csv'

    def parse(self):

        # for i in [292,324,4469,2291,299,2293,301,4470]:
        # for i in [4484,4485,4488,4810,4818,4817,1781,1407,2366,2637,2866,4483,2330,670,2309,671,707]:
        # for i in [373,374,1782,1813,376,377,375,2311,3163,3889,4468,1378]:
        # for i in [381, 1239, 1814, 3580, 2665]:
        for i in self.instance_id:
            url = self.url + str(i)
            res = requests.get(url=url)
            if res.status_code == 200:
                data = eval(res.text)['data']['content']
                # pprint.pprint(data)
                icon = data['icon']
                id = data['id']
                name = data['title']
                summary = data['summary']
                print(summary)
                try:
                    text = data['contents'][0]['text']
                except:
                    text = data['content']
                description = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('秘境简述</td> <td>(.*?)</td>', text)]
                entrance_description = [re.sub('<(.*?)>', '', str(i)) for i in
                                        re.findall('秘境入口简述</td> <td>(.*?)</td>', text)]
                consumption = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('秘境消耗</td> <td>(.*?)</td>', text)]
                online = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('联机</td> <td>(.*?)</td>', text)]
                task = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('任务本</td> <td>(.*?)</td>', text)]
                abnormal_situation = [re.sub('<(.*?)>', '|', str(i)) for i in
                                      re.findall('                (.*?)</p></td></tr>', text)]
                master = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('<br><span>(.*?)</span></a></td>', text)]
                master = list(set(master))
                fix_product = ['摩拉', '冒险阅历']
                if '角色天赋培养素材' in summary:
                    abnormal_situation = [i for i in abnormal_situation[0].split('|') if
                                          re.findall('[\u4e00-\u9fa5]+', i)]
                    date = [re.sub('<(.*?)>', '|', str(i)) for i in
                            re.findall('奖励类型</p></td>(.*?)</p></td></tr>', text)]
                    date = [j for j in date[0].split('|') if j]
                    prob_product = [re.sub('<(.*?)>', '|', str(i)) for i in
                                    re.findall('data-type="obc-content" target="_blank">(.*?)</a></p></td><td', text)]
                    prob_product_cp = []
                    [prob_product_cp.extend([i for i in j.split("|") if re.findall('教导|指引|哲学', i)]) for j in
                     prob_product]
                    prob_product = [set(), set(), set()]
                    [prob_product[i % 3].add(prob_product_cp[i]) for i in range(len(prob_product_cp))]
                    prob_product = [list(i) for i in prob_product]
                    for i in range(0, 6, 2):
                        data.append({'nhy_id': id, 'name': name, 'sec_instance': date[i],
                                     'description': description[0].replace(',', '，'),
                                     'entrance_description': entrance_description[0].replace(',', '，'),
                                     'consumption': consumption[0].replace(',', '，'),
                                     'online': online[0].replace(',', '，'), 'task': task[0].replace(',', '，'),
                                     'date': date[i + 1],
                                     'prob_product': prob_product[i // 2], 'fix_product': fix_product,
                                     'master': master, 'icon': icon,
                                     'abnormal_situation': ''.join(abnormal_situation[:-1]).replace(',', '，'),
                                     'recommended_element': abnormal_situation[-1]})
                elif '武器突破素材' in summary:
                    abnormal_situation = [i for i in abnormal_situation[0].split('|') if
                                          re.findall('[\u4e00-\u9fa5]+', i)]
                    date = [re.sub('<(.*?)>', '|', str(i)) for i in re.findall('）</span></p></td>(.*?)掉落数', text)]
                    date = [j for j in date[0].split('|') if j]
                    prob_product = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('data-type="obc-content" target="_blank">(.*?)</a></p></td><td', text)]
                    prob_product_cp = [set(), set(), set()]
                    [prob_product_cp[i % 3].add(prob_product[i]) for i in range(len(prob_product))]
                    prob_product = [list(i) for i in prob_product_cp]
                    data = []
                    for i in range(0, 6, 2):
                        data.append({'nhy_id': id, 'name': name, 'sec_instance': date[i],
                                     'description': description[0].replace(',', '，'),
                                     'entrance_description': entrance_description[0].replace(',', '，'),
                                     'consumption': consumption[0].replace(',', '，'),
                                     'online': online[0].replace(',', '，'), 'task': task[0].replace(',', '，'),
                                     'date': date[i + 1],
                                     'prob_product': prob_product[i // 2], 'fix_product': fix_product,
                                     'master': master, 'icon': icon,
                                     'abnormal_situation': ''.join(abnormal_situation[:-1]).replace(',', '，'),
                                     'recommended_element': abnormal_situation[-1]})
                elif '试炼秘境' in summary:
                    ext = eval(data['ext'])['c_54']['filter']['text']
                    recommended_element = eval(ext)[-1].replace('推荐元素/', '').replace('元素', '')
                    entrance_description = [re.sub('<(.*?)>', '', str(i)) for i in
                                            re.findall('pre-wrap;">(.*?)</p></td>', text)]
                    data = [{'nhy_id': id, 'name': name, 'sec_instance': '',
                             'description': description[0].replace(',', '，'),
                             'entrance_description': entrance_description[0].replace(',', '，'),
                             'consumption': '',
                             'online': '否',
                             'task': '否',
                             'date': '',
                             'prob_product': '', 'fix_product': fix_product,
                             'master': master, 'icon': icon,
                             'abnormal_situation': '',
                             'recommended_element': recommended_element}]
                elif '圣遗物' in summary:
                    abnormal_situation = [i for i in abnormal_situation[0].split('|') if
                                          re.findall('[\u4e00-\u9fa5]+', i)]

                    prob_product = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('target="_blank">(.*?)</a>', text)]
                    prob_product = list(set(prob_product))

                    data = [{'nhy_id': id, 'name': name, 'sec_instance': '',
                             'description': description[0].replace(',', '，'),
                             'entrance_description': entrance_description[0].replace(',', '，'),
                             'consumption': consumption[0].replace(',', '，'),
                             'online': online[0].replace(',', '，'), 'task': task[0].replace(',', '，'),
                             'date': '',
                             'prob_product': prob_product, 'fix_product': fix_product,
                             'master': master, 'icon': icon,
                             'abnormal_situation': ''.join(abnormal_situation[:-1]).replace(',', '，'),
                             'recommended_element': abnormal_situation[-1]}]

                elif '角色培养素材' in summary:
                    prob_product = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('target="_blank">(.*?)</a>', text)
                                    if len(i) < 15]
                    prob_product = list(set(prob_product))
                    data = [{'nhy_id': id, 'name': name, 'sec_instance': '',
                             'description': description[0].replace(',', '，'),
                             'entrance_description': entrance_description[0].replace(',', '，'),
                             'consumption': consumption[0].replace(',', '，'),
                             'online': online[0].replace(',', '，'), 'task': task[0].replace(',', '，'),
                             'date': '',
                             'prob_product': prob_product, 'fix_product': fix_product,
                             'master': master, 'icon': icon,
                             'abnormal_situation': '',
                             'recommended_element': ''}]
                df = pd.DataFrame(data=data)
                if os.path.exists(self.path):
                    df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                else:
                    df.to_csv(self.path, index=False, encoding='utf-8')
                time.sleep(2)


class OfficialNoticeSpider():
    """
    爬取米有社西风快递员官方公告内容
    """

    def __init__(self):
        self.url = 'https://bbs-api.mihoyo.com/post/wapi/userPost?size=20&uid=75276539'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    def parse(self):
        next_offset = '7605649'
        for i in range(100):
            if next_offset:
                url = self.url + '&offset=' + next_offset
            else:
                url = self.url
            print(url)
            res = requests.get(url, headers=self.header)
            if res.status_code == 200:
                text = json.loads(res.text)
                # pprint.pprint(text)
                my_offset = next_offset
                next_offset = text['data']['next_offset']
                info_list = text['data']['list']
                data = []
                for info in info_list:
                    uid = info['post']['uid']
                    post_id = info['post']['post_id']
                    content = info['post']['content']
                    # print(content)
                    subject = info['post']['subject']
                    structured_content = eval(info['post']['structured_content'])
                    s_content = []
                    for s in structured_content:
                        if "insert" in s:
                            if isinstance(s["insert"], str):
                                s_content.append(s["insert"])
                    data.append({'subject': subject, 'content': content, 'post_id': post_id,
                                 'uid': uid, 's_content': s_content,
                                 'my_offset': my_offset, 'next_offset': next_offset})
                df = pd.DataFrame(data=data)
                if os.path.exists('../rec_intention/notice.csv'):
                    df.to_csv('../rec_intention/notice.csv', mode='a', header=False, index=False, encoding='utf-8')
                else:
                    df.to_csv('../rec_intention/notice.csv', index=False, encoding='utf-8')
            time.sleep(3)


class Strategy():
    """
    攻略区爬虫
    """

    def __init__(self, ):
        self.url = 'https://bbs-api.mihoyo.com/post/wapi/recommendWalkthrough?forum_id=43&gids=2&is_good=false&is_hot=true&size=20'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    def parse(self):
        """
        hot
        :return:
        """
        for i in range(9, 10):
            try:
                res = requests.get(url=self.url + '&offset=' + str(i), headers=self.header)
                if res.status_code == 200:
                    text = json.loads(res.text)
                    # pprint.pprint(text)
                    post = text['data']['posts']
                    data = []
                    for info in post:
                        content = info['post']['content']
                        subject = info['post']['subject']
                        post_id = info['post']['post_id']
                        uid = info['post']['uid']
                        auther = info['user']['nickname']
                        topics = info['topics']
                        topic1, topic2, topic3 = [], [], []
                        for t in topics:
                            if 'content_type' in t and 'name' in t:
                                if t['content_type'] == 1:
                                    topic1.append(t['name'])
                                elif t['content_type'] == 2:
                                    topic2.append(t['name'])
                                elif t['content_type'] == 3:
                                    topic3.append(t['name'])
                        structured_content = eval(info['post']['structured_content'])
                        s_content = []
                        for s in structured_content:
                            if "insert" in s:
                                if isinstance(s["insert"], str):
                                    s_content.append(s["insert"])
                        data.append({'subject': subject, 'content': content, 'post_id': post_id,
                                     'uid': uid, 's_content': s_content, 'auther': auther,
                                     'topic1': topic1, 'topic2': topic2, 'topic3': topic3})
                    print(f"page:{i} got it...")
                    df = pd.DataFrame(data=data)
                    if os.path.exists('../rec_intention/hot_strategy.csv'):
                        df.to_csv('../rec_intention/hot_strategy.csv', mode='a', header=False, index=False,
                                  encoding='utf-8')
                    else:
                        df.to_csv('../rec_intention/hot_strategy.csv', index=False, encoding='utf-8')
                    time.sleep(2)
            except:
                print(f'page {i} is errorrrrrrrrrrrrrr.........')


class Newwest():
    """
    最新发帖
    """

    def __init__(self):
        self.url = 'https://bbs-api.mihoyo.com/post/wapi/getForumPostList?forum_id=43&gids=2&is_good=false&is_hot=false&page_size=20&sort_type=2'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    def parse(self):
        # &last_id=31978671
        last_id = '27964388'
        for i in range(1000):
            try:
                if last_id:
                    url = self.url + "&last_id=" + str(last_id)
                else:
                    url = self.url
                print(f'【page: {i} last_id: {last_id}】is over...')
                res = requests.get(url, headers=self.header)
                if res.status_code == 200:
                    text = json.loads(res.text)
                    # pprint.pprint(text)
                    my_last_id = last_id
                    last_id = text['data']['last_id']
                    info_list = text['data']['list']
                    data = []
                    for info in info_list:
                        uid = info['post']['uid']
                        post_id = info['post']['post_id']
                        content = info['post']['content']
                        # print(content)
                        auther = info['user']['nickname']
                        subject = info['post']['subject']
                        structured_content = eval(info['post']['structured_content'])
                        s_content = []
                        for s in structured_content:
                            if "insert" in s:
                                if isinstance(s["insert"], str):
                                    s_content.append(s["insert"])
                        topics = info['topics']
                        topic1, topic2, topic3 = [], [], []
                        for t in topics:
                            if 'content_type' in t and 'name' in t:
                                if t['content_type'] == 1:
                                    topic1.append(t['name'])
                                elif t['content_type'] == 2:
                                    topic2.append(t['name'])
                                elif t['content_type'] == 3:
                                    topic3.append(t['name'])
                        data.append({'subject': subject, 'content': content, 'post_id': post_id,
                                     'uid': uid, 's_content': s_content, 'auther': auther,
                                     'my_last_id': my_last_id, 'last_id': last_id,
                                     'topic1': topic1, 'topic2': topic2, 'topic3': topic3})
                    df = pd.DataFrame(data=data)
                    if os.path.exists('../rec_intention/最新发帖2.csv'):
                        df.to_csv('../rec_intention/最新发帖2.csv', mode='a', header=False, index=False, encoding='utf-8')
                    else:
                        df.to_csv('../rec_intention/最新发帖2.csv', index=False, encoding='utf-8')
                time.sleep(3)
            except:
                print(f'【page: {i} last_id: {last_id}】 is error...')


class ArtifactsSpider():
    def __init__(self):
        self.url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id='
        self.id = [1563, 1643, 1644, 1645, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1636, 1637, 1638, 1639, 1628, 1629, 1630, 1631, 1632, 1633, 2321, 2322, 1983, 1984, 4341, 4335, 3866, 3867, 3157, 3158]

    def parse(self):
        data = []
        for idd in self.id:
            print(idd)
            url = self.url+str(idd)
            # print(url)
            res = requests.get(url)
            if res.status_code == 200:
                text = json.loads(res.text)
                # pprint.pprint(text)
                name = text['data']['content']['title']
                id = text['data']['content']['id']
                effect = eval(text['data']['content']['ext'])["c_218"]["table"]["list"]
                e = {}
                for i in effect:
                    e[i['key']] = i['value']
                text = text['data']['content']['contents'][0]['text']
                rarity = ''.join([re.sub('<(.*?)>', '', str(i)) for i in
                          re.findall('稀有度</span>(.*?)</p>', text)])
                rarity = rarity.replace(' ','')
                getting = ''.join([re.sub('<(.*?)>', '', str(i)) for i in
                          re.findall('获取途径</span>(.*?)</span>', text)])
                getting = getting.replace(' ','')
                flower = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('<td><label>生之花：</label>(.*?)</td>', text)]
                feather = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('<td><label>死之羽：</label>(.*?)</td>', text)]
                clock = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('<td><label>时之沙：</label>(.*?)</td>', text)]
                cup = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('<td><label>空之杯：</label>(.*?)</td>', text)]
                pileum = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('<td><label>理之冠：</label>(.*?)</td>', text)]
                desc = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('<label>描述：</label>(.*?)</p>', text)]
                img = [re.sub('<(.*?)>', '', str(i)) for i in
                                    re.findall('src="(.*?)"></td>', text)]
                equipment = flower+feather+clock+cup+pileum
                for i in range(5):
                    data.append({'mhy_id':id,'name':equipment[i],'introduction':desc[i],'rarity':rarity,'getting':getting,'icon':img[i],'type':name,'effect':e,'label':'artifacts'})
                # print(data)
                time.sleep(2)
        df= pd.DataFrame(data=data)
        df.to_csv('./aaa.csv',index=False,encoding='utf-8')


    def clear(self):
        df = pd.read_csv('../rec_intention/kg_data/to_do/label-sacred-relic.csv')

        def split_desc(x):
            x = eval(x)
            rarity = x[0]
            x = x[1:]
            dropping, role,  = [], []
            desc,effect = '',''
            for i in x:
                if re.findall('掉落|获取|奖励|概率掉落', str(i)):
                    dropping.append(i.split('：')[0])
                else:
                    # print(len(x),i)
                    idx = x.index(i)
                    # print(idx)
                    x = x[idx:]
                    break

            flag = False
            for i in range(len(x)):
                if '描述' in x[i] and not flag:
                    effect = ''.join(x[:i])
                    flag = True
                elif '描述' in x[i] and flag:
                    desc += x[i].replace('描述：','')
                elif '描述' not in x[i] and flag:
                    role.append(x[i])

            return pd.Series([rarity, dropping, effect, desc, role])

        df[['rarity', 'dropping', 'effect', 'description', 'applicable_roles']] = df['desc'].apply(
            lambda x: split_desc(x))
        df.drop(['desc'],axis=1,inplace=True)
        df.to_csv('../rec_intention/kg_data/done/label-sacred-relic.csv',index=False,encoding='utf-8')
        print(df['rarity'])
        print(df['dropping'])
        print(df['effect'])
        print(df['description'])


if __name__ == "__main__":
    url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id='
    df = pd.read_csv('../rec_intention/kg_data/label-food.csv')
    id = list(set(df['mhy_id'].tolist()))
    result = {}
    for i in id:
        res = requests.get(url+str(i))
        # print(res)
        if res.status_code ==200:
            text = json.loads(res.text)['data']['content']['contents'][0]['text']
            # pprint.pprint(text)
            icon = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('src="(.*?)"></td>', text)]
            name = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('名称：(.*?)</td>', text)]
            for i in range(len(name)):
                n = re.sub('[^\u4e00-\u9fa5]+','',name[i])
                result[n] = icon[i]
    print(result)

    df['icon'] = df['name'].apply(lambda x:result[re.sub('[^\u4e00-\u9fa5]+','',x)])
    df.to_csv('../rec_intention/kg_data/done/label-food2.csv',index=False,encoding='utf-8')


