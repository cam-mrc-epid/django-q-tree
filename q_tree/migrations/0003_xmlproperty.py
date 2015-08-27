# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('q_tree', '0002_auto_20150602_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='XMLProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.IntegerField(db_index=True, choices=[(1, b'Rendering Hint'), (2, b'cssClass'), (3, b'Dynamic'), (4, b'Multi')])),
                ('value', models.CharField(max_length=100, db_index=True)),
                ('q', models.ForeignKey(blank=True, to='q_tree.Question', null=True)),
                ('qg', models.ForeignKey(blank=True, to='q_tree.QuestionGroup', null=True)),
                ('section', models.ForeignKey(blank=True, to='q_tree.Section', null=True)),
                ('tn', models.ForeignKey(blank=True, to='q_tree.TextNode', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
