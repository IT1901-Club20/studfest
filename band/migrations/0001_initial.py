# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 13:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image_filename', models.CharField(blank=True, default='', max_length=210)),
                ('bio_text', models.CharField(default='No bio yet :(', max_length=1400)),
                ('streaming_popularity', models.IntegerField(default=0)),
                ('albums_sold', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='band',
            name='genres',
            field=models.ManyToManyField(related_name='bands', to='band.Genre'),
        ),
        migrations.AddField(
            model_name='band',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
