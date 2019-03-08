# -*- coding: utf-8 -*-

"""
Copyright © 2019-present Lenovo

This file is licensed under both the BSD-3 license for individual/non-commercial use and
EPL-1.0 license for commercial use. Full text of both licenses can be found in
COPYING.BSD and COPYING.EPL files.
"""

# Generated by Django 1.11.10 on 2018-09-18 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

from . import CreatePreferenceData


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default_bill_group', max_length=20, unique=True)),
                ('balance', models.FloatField(default=0)),
                ('charged', models.FloatField(default=0)),
                ('used_time', models.BigIntegerField(default=0)),
                ('used_credits', models.FloatField(default=0)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
                ('charge_rate', models.FloatField(default=1)),
                ('last_operation_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credits', models.FloatField(default=0)),
                ('apply_time', models.DateTimeField(null=True)),
                ('approved_time', models.DateTimeField(null=True)),
                ('bill_group', models.ForeignKey(db_column='bill_group', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.BillGroup')),
            ],
        ),
        migrations.CreateModel(
            name='ImportRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('action_username', models.CharField(max_length=32)),
                ('task_id', models.CharField(max_length=40, null=True)),
                ('username', models.CharField(max_length=32)),
                ('role', models.IntegerField(choices=[(300, b'admin'), (200, b'operator'), (100, b'user')], default=100)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('bill_group_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('status', models.CharField(max_length=24, null=True)),
                ('error_message', models.CharField(max_length=50, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibuserConfig',
            fields=[
                ('key', models.TextField(primary_key=True, serialize=False)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('value', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(error_messages={'username': 'User already exists'}, max_length=32, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('role', models.IntegerField(choices=[(300, b'admin'), (200, b'operator'), (100, b'user')], default=100)),
                ('last_login', models.DateTimeField(null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_operation_time', models.DateTimeField(null=True)),
                ('fail_chances', models.IntegerField(default=0)),
                ('effective_time', models.DateTimeField(auto_now_add=True)),
                ('bill_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bill_members', to='user.BillGroup')),
            ],
        ),
        migrations.AddField(
            model_name='preference',
            name='user',
            field=models.ForeignKey(help_text=b'null:scope is global,otherwise scope is local', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AlterUniqueTogether(
            name='importrecord',
            unique_together=set([('action_username', 'row'), ('action_username', 'username')]),
        ),
        migrations.AddField(
            model_name='deposit',
            name='user',
            field=models.ForeignKey(db_column='user', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('name', 'user')]),
        ),
        CreatePreferenceData(
            name='monitor.policy.node.status',
            value='cpu_core',
        ),
    ]
