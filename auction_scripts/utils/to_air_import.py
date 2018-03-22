#!/user/bin/env python
# -*- coding:utf-8 -*-

"""
导入客户端Air拍品数据
把excel转成csv格式文件

step 1: excel to csv with utf-8
"""

import logging
import copy
import psycopg2
import os
from classes.filter_dict_reader import FilterDictReader
from classes.xls2csv import xls2csv


log = logging.getLogger(__name__)

_connect_args = {'database': 'auction', 'user': 'vincent', 'password': '', 'host': '10.16.60.47', 'port': 5432}

_auction_args = {'activity_id': 26, 'ready_for_auction': 't', 'sub_activity_id': None}


class TableBase(object):
    activity_id = 28
    ready_for_auction = 't'

    def __init__(self, en_filed, cn_field):
        self.en_filed = en_filed
        self.cn_field = cn_field


    @property
    def zip_fields(self):
        return dict(zip(self.en_filed, self.cn_field))

    @property
    def _len_filed(self):
        return len(self.en_filed) + 3

    @property
    def placeholder(self):
        return ','.join(["%s"] * self._len_filed)

    @property
    def field_str(self):
        field_list = copy.copy(self.en_filed)
        field_list.extend(_auction_args.keys())
        return ', '.join('%s' % field for field in field_list)

    def statements(self):

        stmt = 'INSERT INTO antiques (%s) %s (%s)' % (self.field_str, 'VALUES', self.placeholder)
        print stmt
        return stmt

    def insert_data(self, filepath):
        _abs_path = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(_abs_path, 'excel/%s.csv' % self.session)
        xls2csv(filepath, save_path)
        with open(save_path) as csvfile:
            reader = FilterDictReader(csvfile)
            for row in reader:
                if row[self.zip_fields['evaluation']] == '0.0':
                    row[self.zip_fields['evaluation']] = '0'
                data = [row[self.zip_fields[field]].decode('utf-8') for field in self.en_filed]

                # append extra field values
                data.append(_auction_args['activity_id'])
                data.append(self.session)
                data.append(_auction_args['ready_for_auction'])

                self._run_stmt(data)

    def _run_stmt(self, data):
        with psycopg2.connect(**_connect_args) as conn:
            with conn.cursor() as cur:
                cur.execute(self.statements(), data)

    @staticmethod
    def _count(session):
        """
      计算某以专场的拍品的数量
      :param session:
      :return:
      """
        stmt = 'SELECT count(lot) from antiques where activity_id=%s and sub_activity_id=%s'
        with psycopg2.connect(**_connect_args) as conn:
            with conn.cursor() as cur:
                cur.execute(stmt, [_auction_args['activity_id'], session])
                print u'第%s场插入拍品数量是:'% session
                print cur.fetchone()[0]


class ShuHua(TableBase):
    """
    书画一专场类
    usage:
    > filepath = '/Users/py2018/image_test/sh00.csv'
    > c = ShuHua(12)
    > print c.field_str
    > print c.statements()
    > c.insert_data(filepath)
    > c._count(12)

    """

    SHU_HUA_FIELDS = ["lot", "name", "author", "age", "size", "texture", "evaluation"]   # seven elements
    SHU_HUA_CHN = ['图录号', '中文名称', '中文作者', '中文年代', '尺寸', '中文材质', '估价']

    def __init__(self, session):
        self.session = session  # 专场
        super(ShuHua, self).__init__(self.SHU_HUA_FIELDS, self.SHU_HUA_CHN)


class ShuaHuaTwo(TableBase):
    """
    书画专场二
    中文名称后（B）是中文输入状态  需要修改的
    油画专场 通用
    """
    #
    SHU_HUA2_FIELDS = ["lot", "name", "author", "age", "size", "texture", "evaluation", "name2", "author2"]  # seven elements
    SHU_HUA2_CHN = ['图录号', '中文名称', '中文作者', '中文年代', '尺寸', '中文材质', '估价','中文名称二', '中文作者二']

    def __init__(self, session):
        self.session = session  # 专场
        super(ShuaHuaTwo, self).__init__(self.SHU_HUA2_FIELDS, self.SHU_HUA2_CHN)


class Stamp(TableBase):
    """
    邮品专场、 钱币专场
    """
    STAMP_FIELDS = ["lot", "name",  "evaluation"]
    STAMP_CHN = ['图录号', '中文名称', '估价']

    def __init__(self, session):
        self.session = session
        super(Stamp, self).__init__(self.STAMP_FIELDS, self.STAMP_CHN)



class ChiQi(TableBase):
    STAMP_FIELDS = ["lot", "name", '"size"', "evaluation"]
    STAMP_CHN = ['图录号', '中文名称','尺寸', '估价']


class JiZhiBi(TableBase):
    JZB_FIELDS = ["lot", "name", "author", "age", "size", "texture", "evaluation", "name2",
                       "author2"]  # seven elements
    JZB_CHN = ['图录号', '中文名称', '中文作者', '中文年代', '尺寸', '中文材质', '估价', '中文名称二', '中文作者二']


filepath = '/Users/py2018/image_test/yp_v1.xls'
c = Stamp(14)


c.insert_data(filepath)
c._count(14)