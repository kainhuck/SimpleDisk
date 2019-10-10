import tornado.web
from tornado.web import RequestHandler, StaticFileHandler
import shutil

# 上传文件使用
import config
import os

import logging


class StaticFileHandler_(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler_, self).__init__(*args, **kwargs)
        self.xsrf_token


# Vue post请求测试


class VuepostHandler(RequestHandler):
    def get(self):
        name = self.get_query_argument("name", "pig")
        self.write({
            "status_code": 0,
            "type": "GET",
            "yourName": name
        })

    def post(self):
        name = self.get_body_argument("name")
        self.write({
            "status_code": 0,
            "type": "POST",
            "name": name,
            "msg": "hello" + name
        })


# 请求文件/文件夹Handler


class DirpathHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 501:
            msg = "Need to know where you are now"
        elif status_code == 503:
            msg = "path not exits"
        else:
            msg = "unKnow error"
        self.write({
            "status_code": 3,
            "msg": msg
        })

    def get(self):
        where = self.get_query_argument("where", None)  # 获得当前路径
        # print(where)
        if where == "rootPath":
            self.write({
                "status_code": 0,
                "rootPath": config.ROOT_PATH
            })
        else:
            if not where:  # 如果没传入where报错
                self.send_error(501)
            try:
                fileList = os.listdir(where)
                # print(fileList)
                # assert len(fileList)
                '''
                            {
                                "files":[
                                    {"filename": "name1", "type": "dir", "from": "/home"},
                                    {"filename": "name2", "type": "file", "from": "/home"}
                                ]
                            }
                            '''
                info = {}
                files = []
                for eachFile in fileList:
                    files.append({
                        "filename": eachFile,
                        "type": "dir" if os.path.isdir(os.path.join(where, eachFile)) else "file",
                        "from": where
                    })
                info["files"] = files
                info["status_code"] = 0
                info["from"] = where
                self.write(info)
            except:
                self.send_error(502)  # 路径错误


# 上传下载


class UpdownHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 501:  # 文件不存在
            msg = "Not exits"
        elif status_code == 502:
            msg = "Error in upfile"
        elif status_code == 503:
            msg = "illegal path"
        else:
            msg = "Unknow error"
        self.write({
            "status_code": 3,
            "msg": msg
        })

    def get(self):
        filename = self.get_query_argument("filename")  # filename是文件的路径可以直接打开
        # 设置浏览器头
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition',
                        ('attachment; filename=%s' % filename.split("/")[-1]).encode("utf-8"))

        try:
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        except FileNotFoundError:
            self.send_error(501)

    def post(self):
        logging.info("接收到一个post请求")
        filepath = self.get_body_argument("dir")  # 获取文件上传的路径
        if not filepath.startswith(config.ROOT_PATH):
            self.send_error(503)
        fileDict = self.request.files
        try:
            for inputname in fileDict:
                fileArr = fileDict[inputname]
                for fileObj in fileArr:
                    filepath = filepath + "/" + fileObj.filename
                    with open(filepath, "wb") as f:
                        f.write(fileObj.body)
            self.write("<script>alert('ok')</script>")
            self.redirect("/renderFile")
        except:
            self.send_error(502)


# 文件操作


class FileoptHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 501:
            msg = "mkdir error"
        elif (status_code == 502):
            msg = "file illegal"
        else:
            msg = "unkonw error"

        self.write({
            "status_code": 3,
            "msg": msg
        })

    def get(self):
        '''
        Get请求用于创建文件夹，不能创建普通文件
        '''
        dir_path = self.get_query_argument("dir_path")  # 获取要创建的文件夹的全路径
        try:
            os.mkdir(dir_path)
            self.write({"status_code": 0})
        except:
            self.send_error(501)

    def delete(self):
        '''
        删除文件，包括文件夹
        '''
        file_path = self.get_query_argument("file_path")
        try:
            if os.path.isdir(file_path):
                try:
                    os.removedirs(file_path)
                except:
                    shutil.rmtree(file_path)
                self.write({"status_code": 0})
            elif os.path.isfile(file_path):
                os.remove(file_path)
            else:
                self.send_error(502)
        except:
            self.send_error(503)


# 返回磁盘容量


class DisksizeHanddler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 501:
            msg = "error in check disk size"
        self.write({
            "status_code": 3,
            "msg": msg
        })

    def get(self):
        try:
            st = os.statvfs(config.ROOT_PATH)  # 暂时只适用于linux/unix系统
            total_size = int(st.f_blocks * st.f_frsize / 1024 / 1024 / 1024)
            used_size = int(st.f_bavail * st.f_frsize / 1024 / 1024 / 1024)

            self.write({
                "status_code": 0,
                "total_size": total_size,
                "used_size": used_size
            })
        except:
            self.send_error(501)

# 前端测试接口


class ApiTestHandler(RequestHandler):
    def get(self):
        pass

    def post(self):
        status = self.get_body_argument("name")
        print(status)

# 渲染文件视图模板


class RenderFileHandler(RequestHandler):
    def get(self):
        self.render("files.html")
