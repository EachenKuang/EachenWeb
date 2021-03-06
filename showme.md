# Note
## How to user manage.py 
python manage.py + []
- runserver 运行服务
- startapp 建立APP
- makemigrations 创建迁移
- migrate 迁移
- createsuperuser 创建后台超级用户

## 修改模型要更新数据库
python manage.py makemigrations
python manage.py migrate

## 改变model时，对于默认值的设置方法
- 1、直接在字段中使用default字段来设置
```
create_time = models.DateTimeField(default=timezone.now())

```
- 2、在执行```python manage.py makemigrations```时命令行中设置

- 3、对于DateTimeField，可以使用```auto=```来设置
```
create_time = models.DateTimeField(auto_now_add=True) #添加时间
last_update_time = models.DateTimeField(auto_now=True) #修改时间
```
## is_deleted字段
用于表示文章是否被删除，因为数据库的删除操作是比较危险的，所以设置is_deleted字段来控制而不是实际删除
这样的操作可以保证安全性

use:eachen
pass:kuang12345678

## 常用的模板标签
- 循环：for
- 条件：if\ifequal\ifnotequal
- 连接：url
- 模板：block\extends\include
- 注释：{# #}

## 常用的过滤器
日期：
字数截取：truncatechars\truncatechars_html\truncatewords\truncatewords_html
是否信任html：safe
长度：length

## CSS框架
bootstrap
```
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
```
第一条是为了兼容IE
第二条是为了响应式布局

建议JS文件放在body最下面

响应式布局：根据窗口自动响应样式布局

## 分页和shell命令行模式

```
>>> for i in range(1,50):
...     blog.title = "for %s" % i
...     blog.blog_type = blog_type
...     blog.author = user
...     blog.content = "XXXX: %s" % i
...     blog.save()
```

分页器
```
form django.core.paginator import Paginator
paginator = Paginator(object_list, each_page_count)
page1 = paginator(1)
```

内容需要先排序
在model中添加
```
    class Meta:
        ordering = ["-create_time"]
```


- 友好的用户体验
- 当前页高亮
- 不要过多页码选择

```
page_range = [current_page_num + offset for offset in range(-2, 3)
              if 0 < current_page_num + offset <= paginator.num_pages]  # 为了避免出现超过阈值的页码
```

## 上下篇博客和按月分类

### 需求：
在博客详情页中有上一篇与下一篇的链接操作
Django filter

条件中的双下划线

filter()
字段加上后面的状态
- __gt    大于
- __gte   大于等于
- __lt    小于
- __lte   小于等于
- __in    其中之一
- __range 范围
- __contains  包含
- __startwith 开头是
- __endwith   结尾是

eg:`Blog.objects.filter(create_time__gt=blog.create_time).last()`
exclude()
同filter，只不过是filter的逆操作

## 博客分类统计

- 分类统计

  - 方法一：直接计算
    ```
    blog_types_list = []
        for blog_type in blog_types:
            blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
            blog_types_list.append(blog_type)
    ```
  - 方法二：使用annotate

    ```p
    context['blogs_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    ```
    为 BlogType 添加一个字段 blog_count

- 日期归档
    - 直接计算
    ```
    # 获取日期归档对应的博客数量
        blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
        blog_dates_dict = {}
        for blog_date in blog_dates:
            blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                                create_time__month=blog_date.month).count()
            blog_dates_dict[blog_date] = blog_count
    ```
    - 使用annotate
    
## 博客后台富文本编辑

- 简单文本编辑
    - 直接贴入HTML代码
- 富文本编辑
    - 最终解析成HTML
        * 富文本编辑器
        * Markdown编辑器

{{}}中使用过滤
|   
striptags 过滤掉标签
safe 可以解析html

django-ckeditor
- 具有基本的富文本编辑功能
- 可以上传图片
- 可以查看源码
- 有持续更新（维护）

1. 安装
2. 注册应用
3. 配置model
    - 把字段改成RichTextField
    ```
    from ckeditor.fields import RichTextField
    content = RichTextField
    ```
4. 添加上传图片功能
    - 安装
        - pip install pillow
    - 注册应用
        - 'ckeditor_uploader'
    - 配置URL
        ```
        path('ckeditor', include('ckeditor_uploader.urls'))
        urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
        ```
    - 配置model
        - 把字段改成RichTextUploadingField

## 博客阅读简单计数

- 规则：怎样算阅读一次：
1. 无视是否同一个人，每次打开都记录
2. 若同一个人，每隔多久才算阅读一次


- 该计数方法的缺点：
1. 后台编辑博客可能影响数据
2. 功能单一，无法统计某一天的阅读数
3. 无法并发，会出现擦除数据

## 博客阅读计数优化
将read_num抽象出来成为一个model
```
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
```
在blog model中添加一个获得方法
```
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
```
这样就能通过blog.readnum 获取ReadNum model,进而获取对应的read_num
在admin中可以通过方法get_read_num获取

contenttype

## 阅读计数统计和显示

date = timezone.now().date()
read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
read_detail.read_num += 1
read_detail.save()

使用get_or_create


使用[**highcharts**](https://www.hcharts.cn/docs/start-helloworld)来在网页上设置图片

## 热门博客阅读及其缓存

24小时内  今天数据统计
昨日      昨天数据统计
一周
30天

2\每次都计算，耗时
策略：缓存数据，不用每次都计算

setting 中：
```
# 缓存设置
CASHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table'
    }
}
```

使用以下命令创建缓存表
```shell
python manage.py createcachetable
```

## 评论功能设计和用户登录
1、实现评论功能的方式

- 第三方社会化评论插件
- Django评论库 django-comment
- 自己写代码实现

2、创建评论模型
评论对象
评论内容
评论时间
评论者

3、评论需要登录用户
确保较低程度减少垃圾评论
也提高了评论门槛（第三方登录解决）
还可以通知用户

render 与 render_to_response的区别
render比render_to_response需要多一个request
在渲染时，会有默认的user
推荐使用render

## html 表单提交评论
```python
from django.urls import reverse
reverse('home')
```
反向解析使用rerverse，解析别名为'home'的url



## 使用Django Form表单
Django用Form类描述html表单，帮助或简化操作
1、接受和处理用户提交
可检查提交的数据
课将数据转换成Python的数据类型
2、可自动生成html代码
创建form.py文件
字段 html

```
from django.contrib.auth.models import User
username = reg_form.cleaned_data['username']
email = reg_form.cleaned_data['email']
password = reg_form.cleaned_data['password']
user = User.objects.create_user(username, email, password)
user.save()

user = User()
user.username = username
user.email = email
user.set_password(password)
user.save()
```
两种方式保存User

## 富文本编辑和ajax提交评论
1、django-ckeditor富文本表单

可以在github上看到

2、ajax提交


## 回复功能设计和树结构
回复
评论


## 获取评论数和细节处理

- 自定义模板标签
降低耦合，代码更加独立和使用更加简单
templatetags

{% get_comment_list blog as comments %} 重命名不渲染


- 细节处理
1. ajax返回的日期
返回的时间-->时间戳timestamp
2. CSS样式调整
3. 级联删除
4. django-ckeditor

## 点赞功能设计
 博客可以评论、回复可点赞
 可取消点赞
 可看到点赞总数
 
功能需求分析->模型设计->前端初步开发->后端实现->完善前端代码

1、新增评论和回复无法点赞
2、未登录情况下点赞

## 登录与注册
将关于登录与注册的模块集成到user app中
template 中新增user文件夹，登录与注册对应的HTML移动至user

将loginform作为全局调用的写入setting
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.login_modal_form',
            ],
        },
    },
]
```
在TEMPLATES.OPTIONS中的context_processors中添加login_modal_form


## 自定义用户模型
1. 继承Django用户模型：
* 方法
    - 自定义模型继承AbstractUser
    - 配置settings的AUTH_USER_MODEL
* 使用
    - 外键关联settings.AUTH_USER_MODEL
    - 用get_user_model的方法获取User模型

* 优缺点
    - 优点：
      * 自定义强
      * 没有不必要的字段（需要继承AbstractBaseUser）
    - 缺点：
      * 需要删库重来或者要项目一开始就使用
      * 配置admin麻烦

2. 新的模型拓展
* 方法
  - 创建自定义模型
  - 外键关联User

* 使用
  - 直接使用即可
  
* 优缺点
  - 优点
    - 使用方便
    - 不用删库重来影响整体构架
  - 缺点
    - 存在不必要的字段
    - 对比继承的而方法，查询速度稍微慢一点
    
## 邮箱作用
1. 减少垃圾用户
2. 保证账户安全
3. 推送消息

异步发送邮件：
1. 简单方法：多线程
  简单、实现快
2. 复杂方法Celery
  - 可防止任务过多
  - 可定时执行一些任务
  - 开销更大
  
  
##MySQL

mysql -h localhost -u root -p

python manage.py dumpdata > data.json
python manage.py loaddata data.json

create user 'kyc' identified by '123456'
create database EachenWeb default charset=ut8mb4 default collate utf8mb4_inicode_ci
grant all privileges on eachenweb.* to 'kyc';
flush privileges;


如果不需要在程序中特别处理时区（timezone-aware），在Django项目的settings.py文件中，
可以直接设置为“USE_TZ = False”就省心了。
然后，在models.py中简单的设置为“ create_time = models.DateTimeField(auto_now_add=True)”
和“update_time = models.DateTimeField(auto_now=True)”。
如果还要保持USE_TZ=True，则可设置为“default=datetime.now().replace(tzinfo=utc)” 。



## 部署list
1、关闭debug
    多个settings.py文件
    allow_hosts
    使用环境变量设置敏感信息
    日志文件
    404、500错误页面
    发送错误时，邮件通知管理员
2、静态文件
3、设置上传文件目录的权限



检查nginx错误日志(/var/log/nginx/error.log)

/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log

https://eachen.online
https://www.eachen.online
https://myweb.eachen.online
目前这三个网址都可以访问

python manage.py collectstatic


##  第三方登录：
### QQ
http://op.open.qq.com/appregv2/
https://connect.qq.com/manage.html#/
### 微信
开发者资质审核需要300元


##
1、安装uwsgi
注意：
	1）在系统环境安装，非虚拟环境
	2）使用对应python版本安装
	3）要先安装python开发包

pip3 install uwsgi


2、测试 uwsgi 是否正常：
新建 test.py 文件，内容如下：
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"

然后在终端运行：
uwsgi --http :8001 --wsgi-file test.py
注意：需要开启端口才可以正常访问


3、可以用uwsgi的http协议访问django写的网站
执行如下命令可以测试自己的项目
uwsgi --http :8001 --chdir /home/mysite --home /home/mysite_env --module mysite.wsgi:application


4、安装nginx
若有安装过apache，要先把apache服务关闭(apache2ctl stop)
apt-get update
apt-get install nginx

移除default
/etc/nginx/sites-enabled/default

进入sites-available创建新的配置
cd /etc/nginx/sites-available/
vim mysite.conf

配置可以参考下面：
server {
    listen 80;
    server_name mysite;
    charset utf-8;

    client_max_body_size 75M;

    location /static {
        alias /home/mysite/static;
    }

    location /media {
        alias /home/mysite/media;
    }

    location / {
        uwsgi_pass 127.0.0.1:8001;
        include /etc/nginx/uwsgi_params;
    }
}

再设置软链接到sites-enabled
ln -s /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/mysite.conf


5、配置uwsgi，创建ini文件方便处理。ini参考如下：
[uwsgi]
chdir = /home/mysite
home = /home/mysite_env
module = mysite.wsgi:application

master = True
processes = 4
harakiri = 60
max-requests = 5000

socket = 127.0.0.1:8001
uid = 1000
gid = 2000

pidfile = /home/mysite_uwsgi/master.pid
daemonize = /home/mysite_uwsgi/mysite.log
vacuum = True


6、启动uwsgi
uwsgi --ini /home/mysite_uwsgi/mysite.ini


7、重启nginx
service nginx restart


=======================
其他参考：
nginx测试命令：nginx -t
查看uwsgi进程：ps -aux | grep uwsgi
正常关闭uwsgi进程：uwsgi --stop /home/mysite_uwsgi/master.pid
强制关闭全部uwsgi进程：ps -aux | grep uwsgi |awk '{print $2}'|xargs kill -9
重新加载uwsgi：uwsgi --reload /home/mysite_uwsgi/master.pid

参考文档：
（Django官网）https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/uwsgi/
（uwsgi中文）https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/tutorials/Django_and_nginx.html
（uwsgi英文）https://uwsgi.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
（自强学堂）https://code.ziqiangxuetang.com/django/django-nginx-deploy.html

## 第三方登录 QQ
