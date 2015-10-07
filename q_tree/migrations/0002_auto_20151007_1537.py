# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('q_tree', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='position',
            field=models.IntegerField(default=b'0'),
            preserve_default=True,
        ),
    ]
