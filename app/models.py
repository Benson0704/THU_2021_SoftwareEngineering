'''
这个文件定义了后端的11个类
modified: 4.20
'''

from django.db import models


class User(models.Model):
    '''
    用户类
    '''
    open_id = models.TextField(max_length=500, unique=True,
                               primary_key=True)  # 用户id，用户唯一标志
    name = models.TextField(max_length=500, unique=True)  # 用户昵称
    sex = models.BooleanField(null=True)  # 性别设置为bool，1为F，0为M，可空
    head = models.TextField(max_length=500, null=True)  # 头像地址
    bigHead = models.TextField(max_length=500, null=True)  # 大头像地址
    city = models.TextField(max_length=50, null=True)  # 用户地区
    fan = models.IntegerField(default=0)  # 粉丝数
    follow = models.IntegerField(default=0)  # 关注数
    video_count = models.IntegerField(default=0)  # 视频总量
    public_count = models.IntegerField(default=0)  # 公开视频数量
    friend_count = models.IntegerField(default=0)  # 仅好友可见的视频数量
    private_count = models.IntegerField(default=0)  # 仅自己可见的视频数量
    total_like_count = models.IntegerField(default=0)  # 总点赞数
    total_comment_count = models.IntegerField(default=0)  # 总评论数
    total_view_count = models.IntegerField(default=0)  # 总播放数
    access_token = models.TextField(max_length=2500, null=True)
    refresh_token = models.TextField(max_length=2500, null=True)
    identity = models.BooleanField(default=False)  # 表示用户是否为管理员 1:是 0:否
    auth_user = models.TextField(max_length=500000, default="")  # 授权的用户
    authed_user = models.TextField(max_length=500000, default="")  # 谁授权给我

    class Meta:
        '''
        double linking: users
        '''
        db_table = 'users'


class Video(models.Model):
    '''
    视频类
    '''
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='video')  # 用户
    photo_id = models.TextField(max_length=50, primary_key=True)  # 作品id
    caption = models.TextField(max_length=500,
                               default="Default Caption")  # 作品标题
    cover = models.TextField(max_length=500, default="Default Cover")  # 作品封面
    play_url = models.TextField(max_length=500)  # 作品播放链接
    create_time = models.DateTimeField(default=0)  # 作品创建时间
    like_count = models.IntegerField(default=0)  # 作品点赞数
    comment_count = models.IntegerField(default=0)  # 作品评论数
    view_count = models.IntegerField(default=0)  # 作品观看数
    pending = models.BooleanField()  # 作品状态（是否正在处理，不能观看）
    labels = models.TextField(max_length=100, default="", null=True)  # 表示视频的标签

    class Meta:
        '''
        double linking videos
        '''
        db_table = 'videos'


class Label(models.Model):
    '''
    标签类
    '''
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='label')  # 用户
    label_name = models.TextField(max_length=50)  # 标签名
    num = models.IntegerField(default=0)  # 该标签的video数

    class Meta:
        '''
        double linking: labels
        '''
        db_table = 'labels'


class Analyse(models.Model):
    '''
    表示一段时间内数量的统计值(按天统计)
    '''
    video = models.ForeignKey(Video,
                              on_delete=models.CASCADE,
                              related_name='analysis')  # 外键绑定视频
    user_id = models.TextField(max_length=50)  # 用户id
    sum_time = models.DateTimeField(default=0)
    total_view_count = models.IntegerField(default=0)
    total_comment_count = models.IntegerField(default=0)
    total_like_count = models.IntegerField(default=0)

    class Meta:
        '''
        double linking: analysis
        '''
        db_table = 'analysis'


class AnalyseHour(models.Model):
    '''
    表示24h内数量的统计值
    '''
    video = models.ForeignKey(Video,
                              on_delete=models.CASCADE,
                              related_name='analysisHour')  # 外键绑定视频
    user_id = models.TextField(max_length=50)  # 用户id
    sum_time = models.DateTimeField(default=0)
    total_view_count = models.IntegerField(default=0)
    total_comment_count = models.IntegerField(default=0)
    total_like_count = models.IntegerField(default=0)

    class Meta:
        '''
        double linking: analysisHour
        '''
        db_table = 'analysisHour'


class Message(models.Model):
    '''
    消息类，有一个自增的id主键
    '''
    content = models.TextField(max_length=500000,
                               default='default message')  # 消息内容
    title = models.TextField(max_length=1000, default='default title')  # 消息标题
    create_time = models.DateTimeField(default=0)  # 创建时间
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='message')  # 外键绑定用户
    status = models.BooleanField(default=False)  # 消息是否被处理 1:是 0:否
    manager = models.TextField(max_length=1000, null=True)  # 处理的管理员

    class Meta:
        '''
        double linking: message
        '''
        db_table = 'message'


class Feedback(models.Model):
    """
    construct model feedback
    """
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                related_name='feedback')  # 外键绑定消息
    content = models.TextField(max_length=500000,
                               default='default feedback')  # 反馈内容
    title = models.TextField(max_length=1000, default='default title')  # 反馈标题
    create_time = models.DateTimeField(default=0)  # 创建时间
    manager = models.TextField(max_length=1000)  # 管理员
    user = models.TextField(max_length=1000)  # 反馈的用户

    class Meta:
        '''
        double linking: feedback
        '''
        db_table = 'feedback'


class Request(models.Model):
    """
    construct model request
    """
    create_time = models.DateTimeField(default=0)  # 创建时间
    timecost = models.IntegerField(default=0)  # 耗时情况
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='request')  # 外键绑定用户
    request_type = models.TextField(max_length=1000, null=True)  # 请求类型

    class Meta:
        '''
        double linking: request
        '''
        db_table = 'request'


class Notice(models.Model):
    """
    construct model notice
    """
    publish_user = models.TextField(max_length=1000)  # 发布者
    create_time = models.DateTimeField(default=0)  # 创建时间
    content = models.TextField(max_length=500000,
                               default='default feedback')  # 公告内容
    title = models.TextField(max_length=1000, default='default title')  # 公告标题

    class Meta:
        '''
        double linking: notice
        '''
        db_table = 'notice'


class Warn(models.Model):
    """
    construct model warn
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='warn')  # 外键绑定用户
    likes_change = models.IntegerField(default=0)
    comments_change = models.IntegerField(default=0)
    views_change = models.IntegerField(default=0)
    likes_before = models.IntegerField(default=0)
    comments_before = models.IntegerField(default=0)
    views_before = models.IntegerField(default=0)
    warn_time = models.DateTimeField(default=0)  # 预警时间

    class Meta:
        '''
        double linking: warn
        '''
        db_table = 'warn'
