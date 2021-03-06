from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count

from datetime import datetime
from .models import Blog, BlogType
from read_statistics.util import read_statistics_once_read


NUM_BLOG_PER_PAGE = 10


def get_blog_list_common_data(request, blog_all_list):
    paginator = Paginator(blog_all_list, NUM_BLOG_PER_PAGE)
    page_num = request.GET.get('page', 1)  # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前页

    # 获取当前页码前后各两页的页码范围
    page_range = [current_page_num + offset for offset in range(-2, 3)
                  if 0 < current_page_num + offset <= paginator.num_pages]  # 为了避免出现超过阈值的页码

    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = dict()
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blogs_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blog_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context = dict()
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()

    response = render(request, 'blog/blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true', max_age=60, expires=datetime)  # 阅读cookie key
    return response


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request,year, month):
    blog_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)