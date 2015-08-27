# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('q_tree', '0004_auto_20150623_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.IntegerField(db_index=True, choices=[(1, b'Info:cssClass')])),
                ('value', models.CharField(max_length=100, db_index=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('node', models.ForeignKey(blank=True, to='q_tree.BaseTreeNode', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(db_index=True)),
                ('value', models.CharField(max_length=100, db_index=True)),
                ('node', models.ForeignKey(blank=True, to='q_tree.BaseTreeNode', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='css',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='lang',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='xmlproperty',
            name='key',
            field=models.IntegerField(db_index=True, choices=[(1, b'Rendering Hint:tdclass'), (2, b'Rendering Hint:qtype'), (3, b'Rendering Hint:endoftr'), (4, b'Rendering Hint:shownumber'), (5, b'Rendering Hint:table'), (6, b'Rendering Hint:size'), (7, b'search')]),
            preserve_default=True,
        ),
    ]
