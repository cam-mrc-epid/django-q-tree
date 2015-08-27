# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('q_tree', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basetreenode',
            options={'verbose_name': 'Questionnaires', 'verbose_name_plural': 'Questionnaires'},
        ),
        migrations.AddField(
            model_name='questiongroup',
            name='footer',
            field=tinymce.models.HTMLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questiongroup',
            name='header',
            field=tinymce.models.HTMLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='section',
            name='footer',
            field=tinymce.models.HTMLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='section',
            name='header',
            field=tinymce.models.HTMLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questiongroup',
            name='qg_id',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='info',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='q_id',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='subtitle',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='version_date',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='textnode',
            name='t_id',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
