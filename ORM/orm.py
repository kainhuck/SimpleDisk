#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__: kainhuck

from MyMySQL import MyMysql


class ORMMeta(type):
    def __new__(cls, name, bases, attrs):
        '''
        根据属性创造save函数,attrs作为形参
        '''
        if callable('column_list') or 'column_list' not in attrs:
            raise NotImplementedError("必须含有'column_list'属性")

        attrs["save"] = cls.save
        attrs["delete"] = cls.delete
        attrs["update"] = cls.update
        attrs["filter"] = cls.filter
        attrs["getAll"] = cls.getAll
        return type.__new__(cls, name, bases, attrs)

    def save(self, *args):
        '''
        储存数据
        :param args: 对应字段的值
        :return:
        '''
        if not len(args):
            raise Exception("没传参数,储存数据不明确")
        tableName = self.__class__.__name__.lower()
        fieldStr = valueStr = "("
        for field in self.column_list:
            temp = str(field) + ', '
            fieldStr += temp
        fieldStr = fieldStr[:-2] + ")"

        for value in args:
            temp = "'" + str(value) + "', "
            valueStr += temp
        valueStr = valueStr[:-2] + ")"

        sql = "insert into " + tableName + " " + fieldStr + " values " + valueStr + ";"
        # print(sql)
        tempMysql = MyMysql()
        tempMysql.insert(sql)

    def delete(self, **kwargs):
        '''
        删除一条数据
        :param args: 字段对应的值,
                        将删除字段符合这些值的数据
                  exp:       delete from users where user='hello' and pass='sad'
        :usage:
        '''
        tableName = self.__class__.__name__.lower()
        if not len(kwargs):
            sql = 'delete from ' + tableName + ';'
        else:
            fieldStr = ''
            for item in kwargs.items():
                temp = str(item[0]) + "='" + str(item[1]) + "'"
                fieldStr += temp
                fieldStr += ' and '
            sql = 'delete from ' + tableName + ' where ' + fieldStr[:- 5] + ';'
        # print(sql)
        tempMysql = MyMysql()
        tempMysql.delete(sql)

    def update(self, data={}, **kwargs):
        '''
        更新数据库
        :param data: 待更新的数据
        :param kwargs: 查询条件,形参必须是定义的字段
        :return:
        '''
        if not len(data):
            raise Exception("没传参数,无法更新数据")
        elif not isinstance(data, dict):
            raise Exception("data必须为字典类型")
        tableName = self.__class__.__name__.lower()
        fieldStr = conditionsStr = ''
        for item in data.items():
            temp = str(item[0]) + "='" + str(item[1]) + "'"
            fieldStr += temp
            fieldStr += ' and '

        for item in kwargs.items():
            conditionsStr += str(item[0]) + "='" + str(item[1]) + "'"
        sql = 'update ' + tableName + ' set ' + fieldStr[:- 5] + ' where ' + conditionsStr + ';'
        print(sql)
        # tempMysql = MyMysql()
        # tempMysql.delete(sql)

    def getAll(self):
        # "select * from users"
        tableName = self.__class__.__name__.lower()
        sql = "select * from " + tableName
        tempMysql = MyMysql()
        # print(sql)
        return tempMysql.get_all_obj(sql, tableName)

    def filter(self, cname_list=[], limit=-1, offset=0, **kwargs):
        '''
        按条件查询
                SELECT column_name,column_name
                FROM table_name
                [WHERE Clause]
                [LIMIT N][ OFFSET M];

        :param cname_list: 需要查询的字段
        :param limit: 查询上限,默认-1代表无穷
        :param offset: 偏移量,默认0
        :param kwargs: 查询指定条件
        :return:
        '''
        if not len(cname_list):
            raise Exception("没传参数,无法查询数据")

        columnStr = ''
        for column in cname_list:
            columnStr += (column + ",")

        tableName = self.__class__.__name__.lower()
        sql_front = 'select ' + columnStr[:-1] + ' from ' + tableName
        if len(kwargs):
            conditionsStr = ''
            for item in kwargs.items():
                conditionsStr += (str(item[0]) + "='" + str(item[1]) + "'")
            sql_front = 'select ' + columnStr[:-1] + ' from ' + tableName + ' where ' + conditionsStr

        if limit == -1 and offset == 0:
            sql = sql_front + ';'
        elif limit > -1 and offset == 0:
            sql = sql_front + ' limit ' + str(limit) + ';'
        elif limit == -1 and offset > 0:
            raise Exception("定义offset必须定义limit")
        else:
            sql = sql_front + ' limit ' + str(limit) + ' offset ' + str(
                offset) + ';'

        # print(sql)
        tempMysql = MyMysql()
        return tempMysql.get_all_obj(sql, tableName, *cname_list)