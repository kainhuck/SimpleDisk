#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ORM.orm import ORMMeta

'''
使用说明:
以表 t1 为例
一下为表的描述
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| name  | varchar(50) | NO   |     | NULL    |       |
| age   | int(11)     | NO   |     | NULL    |       |
+-------+-------------+------+-----+---------+-------+
'''
# # 必须导入
# from ORM.orm import ORMMeta
#
# # 类名为表名
# class T1(metaclass=ORMMeta):
#     # column_list属性必须定义,里面填入表的字段
#     column_list = ("name", "age")
#
#
# if __name__ == '__main__':
#     a = T1()
#     # a.save("kain", 18)
#     # a.save()  # 错误示范
#     # a.delete(name="kainhcuk", age=18)
#     # a.update(data={"age": 15}, age=12)
#     # print(a.getAll())
#     # print(a.filter(cname_list=["name", "age"], limit=100, offset=10, age=18))

class Tablename(metaclass=ORMMeta):
    column_list = ()