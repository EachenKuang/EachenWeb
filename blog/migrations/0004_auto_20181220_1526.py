# Generated by Django 2.1.4 on 2018-12-20 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20181218_1931'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-create_time']},
        ),
    ]
