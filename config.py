import os
BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {
    'port': 8000,
}

# 数据库配置
mysql = {
    "host": "your_host",
    "user": "your_username",
    "passwd": "your_password",
    "dbName": "your_dbName"
}

# 配置
settings = {
    "static_path": os.path.join(BASE_DIRS, 'static'),
    "template_path": os.path.join(BASE_DIRS, 'templates'),
    "xsrf_cookie": True,
    "cookie_secret": "zadJa2GJTOu5wGL62RngnVrUxVoQ80H2u6qjAfQ4rv4=", # 可自己生成
    "debug": True,  # 调试模式
    "autoescape": None,
    # "login_url": "/login"  # 用户验证失败会映射该路由
}

log_level = "warning"
log_file = os.path.join(BASE_DIRS, "logs/log")

ROOT_PATH = "/SimpTestDir"  # 指定根目录