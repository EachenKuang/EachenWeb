# Generated by Django 2.1.4 on 2019-05-25 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_auto_20181228_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=128)),
                ('oauth_type', models.IntegerField(choices=[(0, 'QQ'), (1, 'WeChat'), (2, 'Sina'), (3, 'Github')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
