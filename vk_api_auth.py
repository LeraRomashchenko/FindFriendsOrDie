import vk
from configparser import ConfigParser

def login_to_api(log):
    config = ConfigParser()
    config.read("settings.ini")
    log.info("read config")
    auth = dict(config.items("auth"))
    log.info("auth app=%s, login=%s" % (auth["app_id"], auth["user_login"]))
    session = vk.AuthSession(app_id=auth["app_id"], user_login=auth["user_login"], user_password=auth["user_password"], scope='photos,friends')
    log.info("authorized")
    api = vk.API(session, v='5.35', lang='en')
    log.info("created api")
    return api
