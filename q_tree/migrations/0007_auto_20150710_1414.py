# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('q_tree', '0006_optionproperty_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xmlproperty',
            name='key',
            field=models.IntegerField(db_index=True, choices=[(1, b'Rendering Hint:tdclass'), (2, b'Rendering Hint:qtype'), (3, b'Rendering Hint:endoftr'), (4, b'Rendering Hint:shownumber'), (5, b'Rendering Hint:table'), (6, b'Rendering Hint:size'), (7, b'search'), (8, b'multi')]),
            preserve_default=True,
        ),
    ]
