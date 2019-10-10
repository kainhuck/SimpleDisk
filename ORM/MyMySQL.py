#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__: kainhuck

import pymysql
import config


class MyMysql():
    def __init__(self):
        self.host = config.mysql['host']
        self.user = config.mysql['user']
        self.passwd = config.mysql['passwd']
        self.dbName = config.mysql['dbName']

    def connect(self):
        self.db = pymysql.connect(self.host, self.user, self.passwd, self.dbName)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def get_one(self, sql):
        '''
        获取第一条数据
        :param sql:
        :return:
        '''
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print('查询失败')
        return res

    def get_all(self, sql):
        '''
        获取全部的数据
        '''
        res = ()
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except:
            print("查询失败")
        return res

    def get_all_obj(self, sql, tableName, *args):
        '''
        以字典形式返回,可以指定返回的字段
        :param args: 指定返回的字段,无则全返回
        '''
        resList = []  # 存放结果
        fieldsList = []  # 存放表头
        fieldAll = []
        fieldSql = "SELECT COLUMN_NAME FROM \
                    information_schema.COLUMNS \
                    WHERE TABLE_NAME = '%s' AND table_schema = '%s'" % (
            tableName, self.dbName
        )
        fields = self.get_all(fieldSql)
        for item in fields:
            fieldAll.append(item[0])

        if len(args):  # 如果指定域
            for item in args:
                fieldsList.append(item)
        else:
            fieldsList = fieldAll

        # 执行查询数据sql
        res = self.get_all(sql)
        for item in res:
            obj = {}
            for x in fieldsList:
                obj[x] = item[fieldAll.index(x)]
            resList.append(obj)
        return resList

    def insert(self, sql):
        return self._exec(sql)

    def update(self, sql):
        return self._exec(sql)

    def delete(self, sql):
        return self._exec(sql)

    def _exec(self, sql):
        '''
        执行sql语句
        :param sql: sql 语句
        '''
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except:
            print("语句提交失败")
            self.db.rollback()
        return count


if __name__ == '__main__':
    mysql = MyMysql()
    print(mysql.get_all_obj("SELECT * FROM t1", "t1"))
    # print(mysql.get_all("SELECT * FROM t1"))
