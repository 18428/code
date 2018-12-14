import base64
import json
import time
import urllib
import uuid


from django.http import HttpResponseRedirect, request, HttpResponse
from django.shortcuts import render, render_to_response


from oauth_server import settings


def login(request):
    return render(request, 'login.html')


def login_action(request):
    errors =[]
    userName = None
    password = None
    if request.method == "POST":
        userName = request.POST.get('userName')
        password = request.POST.get('password')

    # return render(request, 'success.html', {'userName': userName, 'password': password})
    response = render_to_response('success.html', {'userName': userName, 'password': password, 'clientId': '3119f2cfaba8fae78dc0', 'clientSecret': 'fce588b67f746578afe1703143eeeec65e369bb4'})
    response.set_cookie('oauth_cookie', uuid.uuid4())
    return response


class OAuth_Base(object):
    def __init__(self, client_id, client_key, redirect_url):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def _get(self, url, data):
        request_url = '%s?%s' % (url, urllib.parse.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    def _post(self, url, data):
        request = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(encoding='UTF8'))
        response = urllib.request.urlopen(request)
        return response.read()


class OAuth_GITHUB(OAuth_Base):
    def get_auth_url(self):
        params = {'client_id':self.client_id, 'response_type': 'code', 'redirect_uri': self.redirect_url, 'scope': 'user:email', 'state': 1}
        url = 'https://github.com/login/oauth/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self,code):
        params = { 'grant_type':'authorization_code', 'client_id':self.client_id, 'client_secret':self.client_key, 'code': code, 'redirect_url': self.redirect_url}
        response = self._post('https://github.com/login/oauth/access_token', params)
        result = urllib.parse.parse_qs(response,True)
        self.access_token = result[b'access_token'][0]
        return self.access_token

    def get_user_info(self):
        params ={'access_token': self.access_token}
        response = self._get('https://api.github.com/user', params)
        result = json.loads(response.decode('utf-8'))
        self.openid = result.get('id', '')
        return result

    def get_email(self):
        params ={'access_token':self.access_token}
        response = self._get('https://api.github.com/user/emails', params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']

    def get_repo(self):
        params = {'access_token': self.access_token}
        # userName 动态拼接
        response = self._get('https://api.github.com/users/inspurodoo/repos', params)
        result = json.loads(response.decode('utf-8'))
        return result

    def get_repo_detail(self):
        params = {'access_token': self.access_token}
        response = self._get('https://api.github.com/repos/inspurodoo/odoo-reportbro', params)
        result = json.loads(response.decode('utf-8'))
        return result

    def get_commits(self):
        params = {'access_token': self.access_token}
        response = self._get('https://api.github.com/repos/inspurodoo/odoo-reportbro/commits', params)
        result = json.loads(response.decode('utf-8'))
        return result



def git_login(request): #获取code 
    oauth_git = OAuth_GITHUB(settings.GITHUB_APP_ID,settings.GITHUB_KEY,settings.GITHUB_CALLBACK_URL) 
    url = oauth_git.get_auth_url()
    # url = 'https://github.com/login/oauth/authorize?client_id=3119f2cfaba8fae78dc0'
    return HttpResponseRedirect(url)




def git_check(request):
    type='1'
    request_code = request.GET.get('code')
    oauth_git = OAuth_GITHUB(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_CALLBACK_URL)
    try:
        access_token = oauth_git.get_access_token(request_code)
        time.sleep(0.1)
    except:
        data={}
        data['goto_url'] = '/'
        data['goto_time'] = 10000
        data['goto_page'] = True
        data['message_title'] = '登录失败'
        data['message'] = '获取授权失败，请确认是否允许授权，并重试。若问题无法解决，请联系网站管理人员'
        # return render_to_response('oauth/response.html',data)

    infos = oauth_git.get_user_info() #获取用户信息
    nickname = infos.get('login','')
    image_url = infos.get('avatar_url','')
    open_id = str(oauth_git.openid)
    signature = infos.get('bio','')
    if not signature:
        signature = "无个性签名"
    # sex = '1'
    # githubs = OAuth_ex.objects.filter(openid=open_id,type=type)
    #     if githubs:
    #         auth_login(request,githubs[0].user,backend='django.contrib.auth.backends.ModelBackend')
    #         return HttpResponseRedirect('/')
    #     else:
    #         try:
    #             email = oauth_git.get_email()
    #         except:
    #             url = "%s?nickname=%s&openid=%s&type=%s&signature=%s&image_url=%s&sex=%s" % (reverse('oauth:bind_email'),nickname,open_id,type,signature,image_url,sex)
    #             return HttpResponseRedirect(url)
    #     users = User.objects.filter(email=email)
    #     if users:
    #         user = users[0]
    #     else:
    #         while User.objects.filter(username=nickname):
    #                 nickname = nickname + '*'
    #         user = User(username=nickname,email=email,sex=sex,signature=signature)
    #         pwd = str(uuid.uuid1())
    #         user.set_password(pwd)
    #         user.is_active = True
    #         user.download_image(image_url,nickname)
    #         user.save()
    #     oauth_ex = OAuth_ex(user = user,openid = open_id,type=type)
    #     oauth_ex.save()
    #     auth_login(request,user,backend='django.contrib.auth.backends.ModelBackend')
    #     data={}
    #     data['goto_url'] = '/'
    #     data['goto_time'] = 10000
    #     data['goto_page'] = True
    #     data['message_title'] = '绑定用户成功'
    #     data['message'] = u'绑定成功！您的用户名为：<b>%s</b>。您现在可以同时使用本站账号和此第三方账号登录本站了！' % nickname
    #     return render_to_response('oauth/response.html',data)
    return HttpResponse('Hello Giter: %s ,<br> Access token: %s' % (infos['name'], bytes.decode(access_token)))
