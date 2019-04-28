# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-05 05:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('item_id', models.IntegerField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(default=None, max_length=200)),
                ('item_category', models.CharField(default=None, max_length=200)),
                ('item_brand', models.CharField(default=None, max_length=200)),
                ('item_price', models.FloatField(default=None)),
            ],
            options={
                'db_table': 'Items',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('trans_id', models.IntegerField(primary_key=True, serialize=False)),
                ('cust_id', models.IntegerField(default=None)),
                ('date', models.DateField(default=None)),
                ('time', models.TimeField(default=None)),
                ('total_amount', models.FloatField(default=None)),
            ],
            options={
                'db_table': 'Transaction',
            },
        ),
        migrations.CreateModel(
            name='Transaction_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number_of_items', models.IntegerField(default=None)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaarapp.Items')),
                ('trans_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaarapp.Transaction')),
            ],
            options={
                'db_table': 'Transaction_item',
            },
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mobile', models.IntegerField(default=None, unique=True)),
                ('address', models.CharField(default=None, max_length=200)),
                ('state', models.CharField(default=None, max_length=30)),
                ('pincode', models.IntegerField(default=None)),
                ('country', models.CharField(default=None, max_length=30)),
            ],
            options={
                'db_table': 'UserTable',
            },
        ),
    ]
