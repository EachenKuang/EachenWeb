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

