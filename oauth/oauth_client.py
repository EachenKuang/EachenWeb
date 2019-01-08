import json
from urllib import request, parse


class OAuthBase:
    def __init__(self, kw):
        if not isinstance(kw, dict):
            raise Exception("arg is not dict type")

        for key, value in kw.items():
            setattr(self, key, value)

    @staticmethod
    def get_oauth(**kw):
        """静态方法，根据参数实例化对应的类"""
        type_name = kw.get('type_name')

        if type_name == "Github":
            oauth = OAuthGithub(kw)
        else:
            oauth = None
        return oauth

    def _get(self, url, data):
        """get请求"""
        request_url = '%s?%s' % (url, parse.urlencode(data))
        response = request.urlopen(request_url)
        return response.read()

    def _post(self, url, data):
        """post请求"""
        data = bytes(parse.urlencode(data), encoding='utf8')
        response = request.urlopen(url, data=data)
        return response.read()

    # 根据情况重写以下方法
    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': self.scope,
                  'state': self.state}
        return '%s?%s' % (self.url_authorize, parse.urlencode(params))

    # 继承的类要实现下面的方法
    def get_access_token(self, code):
        """根据code获取access_token"""
        pass

    def get_open_id(self):
        """获取用户的标识ID"""
        pass

    def get_user_info(self):
        """获取用户资料信息"""
        pass

    def get_email(self):
        """获取邮箱"""
        pass


class OAuthGithub(OAuthBase):
    openid = ''

    def get_access_token(self, code):
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'code': code,
                  'redirect_uri': self.redirect_uri}

        # Github此处是POST请求
        response = self._post(self.url_access_token, params)

        # 解析结果
        result = parse.parse_qs(response, True)
        self.access_token = result['access_token'][0]
        return self.access_token

    def get_open_id(self):
        """获取用户的标识ID"""
        if not self.openid:
            # 若没有openid，则调用一下获取用户信息的方法
            self.get_user_info()

        return self.openid

    def get_user_info(self):
        """获取用户资料信息"""
        params = {'access_token': self.access_token, }
        response = self._get(self.url_user_info, params)

        result = json.loads(response)
        self.openid = result.get('id', '')
        return result

    def get_email(self):
        """获取邮箱"""
        params = {'access_token': self.access_token, }
        response = self._get(self.url_email, params)

        result = json.loads(response)
        return result[0]['email']
