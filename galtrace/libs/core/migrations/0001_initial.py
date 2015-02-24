# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import galtrace.libs.core.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('vendor', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=15)),
                ('uri', models.CharField(max_length=65535)),
                ('thumb', models.ImageField(max_length=65535, null=True, upload_to=galtrace.libs.core.models.get_image_name)),
                ('phase', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
