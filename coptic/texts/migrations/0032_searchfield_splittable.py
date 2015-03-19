# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0031_remove_htmlvisualization_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchfield',
            name='splittable',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
    ]
