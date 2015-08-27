# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('q_tree', '0005_auto_20150630_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionproperty',
            name='text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
