# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 22:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('band', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('time', models.DateTimeField(verbose_name='Time and date')),
                ('needs', models.CharField(max_length=2048, null=True)),
                ('band', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='band.Band')),
                ('organiser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organiser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=200)),
                ('notes', models.CharField(max_length=2048)),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concert.Concert')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200, null=True)),
                ('notes', models.CharField(max_length=2048, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='concert',
            name='stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='concert.Stage'),
        ),
        migrations.AddField(
            model_name='concert',
            name='techs',
            field=models.ManyToManyField(related_name='technicians', through='concert.Employment', to=settings.AUTH_USER_MODEL),
        ),
    ]