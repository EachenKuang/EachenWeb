from django.contrib import admin
from .models import OAuth_type, OAuth_ex


@admin.register(OAuth_type)
class OAuthTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name', 'title', 'img')

    # 分组表单
    fieldsets = (
        ('OAuth类型信息', {
            "fields": ('type_name', 'title', 'img')
            }),
        ('OAuth基本设置', {
            "fields": ('client_id', 'client_secret', 'redirect_uri', 'scope')
            }),
        ('OAuth请求链接', {
            "fields": ('url_authorize', 'url_access_token', 'url_open_id', 'url_user_info', 'url_email')
            })
    )


@admin.register(OAuth_ex)
class OAuthAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'openid','oauth_type')
