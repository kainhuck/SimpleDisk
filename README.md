# SimpleDisk
用tornado实现的远程文件管理系统（网盘）



## 安装tornado

```
pip3 install tornado
```



## 更改所管理的文件的根目录

分别位于 **config.py** 末行和**templates/files.html**的201行

请注意：**这两个目录必须相同**



## 运行

```shell
# git clone https://github.com/kainhuck/SimpleDisk.git
# cd SimpleDisk
# nohup python3 ./server.py > ./logs/log 2>&1 &
```



## 访问

浏览器中输入 <你的IP地址>:8000



## 一些未解决的BUG

作者前端功力有限（这个项目是现学现做），难免会有一些BUG，目前有这么些为完成的功能或BUG

- index页面未设计，只是简单的一个入口链接
- 下载文件时不能下载多个，如果选择多个默认下载最后一个
- info组件暂未开发
- 待补充...



***项目所用的模板请看[这里](https://github.com/kainhuck/tornado_project_template_for_vue)***



### 如果您对这个项目有兴趣，欢迎加入

**联系我**

> QQ :fist_right:  :one::six::two::eight::three::two::one::two::six::four:













