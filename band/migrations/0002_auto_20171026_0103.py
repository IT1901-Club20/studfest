# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 23:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='band',
            old_name='bioText',
            new_name='bio_text',
        ),
        migrations.RenameField(
            model_name='band',
            old_name='imageFilename',
            new_name='image_filename',
        ),
    ]
