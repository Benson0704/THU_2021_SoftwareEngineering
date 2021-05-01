# Generated by Django 3.1.7 on 2021-04-30 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api', models.CharField(max_length=500)),
                ('P99', models.IntegerField(default=0)),
                ('qps', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'performance',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField()),
                ('timecost', models.IntegerField(default=0)),
                ('request_type', models.TextField(max_length=1000, null=True)),
            ],
            options={
                'db_table': 'request',
            },
        ),
    ]
