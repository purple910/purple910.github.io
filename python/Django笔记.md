# Django笔记



# 配置 jinja2
## 修改模板名
```
TEMPLATES: 
    'BACKEND': 'django.template.backends.jinja2.Jinja2'
```
## 注释掉admin (jinja2没有admin)
```
# 'django.contrib.admin',
# path('admin/', admin.site.urls),
```
## 创建Jinja2环境配置函数
```
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

def jinja2_environment(**options):
    """创建 jinja2 环境对象"""
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
```
## 导入jinja2的配置
```
TEMPLATES 
    'environment': 'woniumall.utils.jinja2_env.jinja2_environment'
```

# 配置session,cookie的有效期
```
# 没有记住用户：浏览器会话结束就过期
request.session.set_expiry(0)
# 记住用户：None表示两周后过期
request.session.set_expiry(None)
# 设置cookie 为关闭浏览器则有效期结束
response.set_cookie('username', user.username)
# 登录时用户名写入到cookie，有效期14天
response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
```

# 配置reverse
## 全局的urls
```
re_path(r'^', include(('areas.urls', 'areas')))
```
## 局部的urls
```
re_path(r'^addresses/$', views.AddressView.as_view(), name='address'),
re_path(r'^aaa',views.Aa.as_view())
```
## view
```
class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_site.html')

class Aa(View):
    def get(self, request):
        # return redirect('/addresses/')
        return redirect(reverse('areas:address'))
```

# authenticate 多用户登录(用户名,手机号)
## 配置认证后端
```
# settings/dev.py
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'users.auth_backend.MobilePasswordBackend']
```
## 创建自定义认证后端
```
# auth_backend.py
class MobilePasswordBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        mobile = kwargs.get('username')
        password = kwargs.get('password')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return

        try:
            # 通过手机号查询数据库
            user = UserModel.objects.get(mobile=mobile)
        except UserModel.DoesNotExist:
            return

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user
```
## 运行流程
```
1 加载 dev.py
2 触发 users.views.LoginView
    user = authenticate(username=username, password=password)
3 循环 _get_backends(return_tuples=True) # 到AUTHENTICATION_BACKENDS里面去循环,默认有一个(ModelBackend)
4 先到 django.contrib.auth.backends.ModelBackend里, 用username到数据库里找
5 没有找到, 返回循环 _get_backends(return_tuples=True)
6 再到 users.auth_backend.MobilePasswordBackend里, 用mobile在数据里找
```

# 实现状态保持(login)
```
在认证用户(authenticate)时,会自动配置认证后端(backend),再实现状态保持(login)时,认证后端(backend)会自动绑定再用户身上;
如果没有进行认证用户(authenticate)时,用户身上则没有认证后端(backend),则要实现状态保持(login)时,就要手动绑定认证后端(backend)
```

# 跨域问题(二选一)
```
1. 再返回时设置response的请求头
   response = render(request, 'register.html')
   response["Access-Control-Allow-Origin"] = '*'
   return response
2. 可以再配置文件配置跨域
    a) pip install django-core-header
    b) INSTALLED_APPS 里面添加 corsheaders 
    c) MIDDLEWARE 里面添加 corsheaders.middleware.CorsMiddleware,django.middleware.common.CommonMiddleware
    d) CORS_ORIGIN_ALLOW_ALL = True, CORS_ALLOW_CREDENTIALS = True
    e) 配置允许访问的连接 CORS_ORIGIN_WHITELIST = ('http://127.0.0.1:8080', 'http://localhost:8080', 'http://www.meiduo.site:8080',)
    f) 配置访问方式 CORS_ALLOW_METHODS = ('DELETE','GET','OPTIONS','PATCH','POST','PUT','VIEW',)
    g) 配置允许访问的请求头
    CORS_ALLOW_HEADERS = (
        'XMLHttpRequest',
        'X_FILENAME',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
        'Pragma',
    )
```

# cookie无妨传递
```
// 是否允许携带cookie
axios.withCredentials = true;
axios.defaults.withCredentials = true
// 若127.0.0.1:8000可以而www.meiduo.site:8000不可以
则是因为前端的host被设置为 127.0.0.1:8000,修改前端的host
```