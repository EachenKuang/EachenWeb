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