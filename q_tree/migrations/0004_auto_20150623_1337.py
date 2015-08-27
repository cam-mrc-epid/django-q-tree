# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('q_tree', '0003_xmlproperty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xmlproperty',
            name='q',
        ),
        migrations.RemoveField(
            model_name='xmlproperty',
            name='qg',
        ),
        migrations.RemoveField(
            model_name='xmlproperty',
            name='section',
        ),
        migrations.RemoveField(
            model_name='xmlproperty',
            name='tn',
        ),
        migrations.AddField(
            model_name='xmlproperty',
            name='node',
            field=models.ForeignKey(blank=True, to='q_tree.BaseTreeNode', null=True),
            preserve_default=True,
        ),
    ]
