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