# Generated by Django 3.1.7 on 2021-04-30 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_user', models.TextField(max_length=1000)),
                ('create_time', models.DateTimeField(default=0)),
                ('content', models.TextField(default='default feedback', max_length=500000)),
                ('title', models.TextField(default='default title', max_length=1000)),
            ],
            options={
                'db_table': 'notice',
            },
        ),
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
        migrations.CreateModel(
            name='User',
            fields=[
                ('open_id', models.CharField(max_length=250, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('sex', models.BooleanField(null=True)),
                ('head', models.CharField(max_length=500, null=True)),
                ('bigHead', models.CharField(max_length=500, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('fan', models.IntegerField(default=0)),
                ('follow', models.IntegerField(default=0)),
                ('video_count', models.IntegerField(default=0)),
                ('public_count', models.IntegerField(default=0)),
                ('friend_count', models.IntegerField(default=0)),
                ('private_count', models.IntegerField(default=0)),
                ('total_like_count', models.IntegerField(default=0)),
                ('total_comment_count', models.IntegerField(default=0)),
                ('total_view_count', models.IntegerField(default=0)),
                ('access_token', models.CharField(max_length=2500, null=True)),
                ('refresh_token', models.CharField(max_length=2500, null=True)),
                ('identity', models.BooleanField(default=False)),
                ('auth_user', models.TextField(default='', max_length=500000)),
                ('authed_user', models.TextField(default='', max_length=500000)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Warn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes_change', models.IntegerField(default=0)),
                ('comments_change', models.IntegerField(default=0)),
                ('views_change', models.IntegerField(default=0)),
                ('likes_before', models.IntegerField(default=0)),
                ('comments_before', models.IntegerField(default=0)),
                ('views_before', models.IntegerField(default=0)),
                ('warn_time', models.DateTimeField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warn', to='app.user')),
            ],
            options={
                'db_table': 'warn',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('photo_id', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('caption', models.CharField(default='Default Caption', max_length=500)),
                ('cover', models.CharField(default='Default Cover', max_length=500)),
                ('play_url', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('view_count', models.IntegerField(default=0)),
                ('pending', models.BooleanField()),
                ('labels', models.CharField(default='', max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to='app.user')),
            ],
            options={
                'db_table': 'videos',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='default message', max_length=500000)),
                ('title', models.TextField(default='default message', max_length=1000)),
                ('create_time', models.DateTimeField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('manager', models.TextField(max_length=1000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='app.user')),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=50)),
                ('num', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='label', to='app.user')),
            ],
            options={
                'db_table': 'labels',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='default feedback', max_length=500000)),
                ('title', models.TextField(default='default title', max_length=1000)),
                ('create_time', models.DateTimeField(default=0)),
                ('manager', models.TextField(max_length=1000)),
                ('user', models.TextField(max_length=1000)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='app.message')),
            ],
            options={
                'db_table': 'feedback',
            },
        ),
        migrations.CreateModel(
            name='AnalyseHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=250)),
                ('sum_time', models.DateTimeField(default=0)),
                ('total_view_count', models.IntegerField(default=0)),
                ('total_comment_count', models.IntegerField(default=0)),
                ('total_like_count', models.IntegerField(default=0)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysisHour', to='app.video')),
            ],
            options={
                'db_table': 'analysisHour',
            },
        ),
        migrations.CreateModel(
            name='Analyse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=250)),
                ('sum_time', models.DateTimeField(default=0)),
                ('total_view_count', models.IntegerField(default=0)),
                ('total_comment_count', models.IntegerField(default=0)),
                ('total_like_count', models.IntegerField(default=0)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis', to='app.video')),
            ],
            options={
                'db_table': 'analysis',
            },
        ),
    ]
