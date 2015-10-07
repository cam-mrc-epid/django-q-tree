# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import polymorphic_tree.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTreeNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'Questionnaires',
                'verbose_name_plural': 'Questionnaires',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalProgram',
            fields=[
                ('basetreenode_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='q_tree.BaseTreeNode')),
                ('position', models.IntegerField()),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
            },
            bases=('q_tree.basetreenode',),
        ),
        migrations.CreateModel(
            name='InfoProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.IntegerField(db_index=True, choices=[(1, b'Info:cssClass')])),
                ('value', models.CharField(max_length=100, db_index=True)),
                ('text', models.TextField(null=True, blank=True)),
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
                ('text', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('basetreenode_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='q_tree.BaseTreeNode')),
                ('var_name', models.CharField(max_length=20)),
                ('position', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
            bases=('q_tree.basetreenode',),
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('basetreenode_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='q_tree.BaseTreeNode')),
                ('position', models.IntegerField()),
                ('qg_id', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Question Group',
                'verbose_name_plural': 'Question Groups',
            },
            bases=('q_tree.basetreenode',),
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('basetreenode_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='q_tree.BaseTreeNode')),
                ('lang', models.CharField(max_length=50, null=True, blank=True)),
                ('css', models.CharField(max_length=50, null=True, blank=True)),
                ('author', models.CharField(max_length=50)),
                ('study_name', models.CharField(max_length=50)),
                ('version_number', models.CharField(max_length=50)),
                ('version_date', models.CharField(max_length=50, null=True, blank=True)),
                ('subtitle', models.CharField(max_length=50, null=True, blank=True)),
                ('info', models.CharField(max_length=50, null=True, blank=True)),
                ('q_id', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Questionnaire',
                'verbose_name_plural': 'Questionnaires',
            },
            bases=('q_tree.basetreenode',),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('basetreenode_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='q_tree.BaseTreeNode')),
                ('position', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
            bases=('q_tree.basetreenode',),
        ),
        migrations.CreateModel(
            name='TextNode',
            fields=[
                ('basetreenode_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='q_tree.BaseTreeNode')),
                ('t_id', models.CharField(max_length=10, null=True, blank=True)),
                ('position', models.IntegerField()),
            ],
            options={
                'verbose_name': 'text Node',
                'verbose_name_plural': 'Text Nodes',
            },
            bases=('q_tree.basetreenode',),
        ),
        migrations.CreateModel(
            name='XMLProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.IntegerField(db_index=True, choices=[(1, b'Rendering Hint:tdclass'), (2, b'Rendering Hint:qtype'), (3, b'Rendering Hint:endoftr'), (4, b'Rendering Hint:shownumber'), (5, b'Rendering Hint:table'), (6, b'Rendering Hint:size'), (7, b'search'), (8, b'multi')])),
                ('value', models.CharField(max_length=100, db_index=True)),
                ('node', models.ForeignKey(blank=True, to='q_tree.BaseTreeNode', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='optionproperty',
            name='node',
            field=models.ForeignKey(blank=True, to='q_tree.BaseTreeNode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infoproperty',
            name='node',
            field=models.ForeignKey(blank=True, to='q_tree.BaseTreeNode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basetreenode',
            name='parent',
            field=polymorphic_tree.models.PolymorphicTreeForeignKey(related_name='children', verbose_name='parent', blank=True, to='q_tree.BaseTreeNode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basetreenode',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_q_tree.basetreenode_set+', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
