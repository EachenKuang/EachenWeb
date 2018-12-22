import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from read_statistics.util import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from django.urls import reverse


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gt=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    week_hot_data = cache.get('week_hot_data')
    if week_hot_data is None:
        week_hot_data = get_7_days_hot_blogs()
        cache.set('week_hot_data', week_hot_data, 3600)  # 设置成一小时

    context = dict()
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['week_hot_data'] = week_hot_data
    return render(request, 'home.html', context)


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确'})