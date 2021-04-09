'''
这个文件定义了后端的两个类
'''

from django.db import models


class User(models.Model):
    '''
    用户类
    '''
    open_id = models.CharField(max_length=50, unique=True,
                               primary_key=True)  # 用户id，用户唯一标志
    name = models.CharField(max_length=50, unique=True)  # 用户昵称
    sex = models.BooleanField(null=True)  # 性别设置为bool，1为F，0为M，可空
    head = models.CharField(max_length=500, null=True)  # 头像地址
    bigHead = models.CharField(max_length=500, null=True)  # 大头像地址
    city = models.CharField(max_length=50, null=True)  # 用户地区
    fan = models.IntegerField(default=0)  # 粉丝数
    follow = models.IntegerField(default=0)  # 关注数
    video_count = models.IntegerField(default=0)  # 视频总量
    public_count = models.IntegerField(default=0)  # 公开视频数量
    friend_count = models.IntegerField(default=0)  # 仅好友可见的视频数量
    private_count = models.IntegerField(default=0)  # 仅自己可见的视频数量
    total_like_count = models.IntegerField(default=0)  # 总点赞数
    total_comment_count = models.IntegerField(default=0)  # 总评论数
    total_view_count = models.IntegerField(default=0)  # 总播放数
    access_token = models.CharField(max_length=2500, null=True)
    refresh_token = models.CharField(max_length=2500, null=True)

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
    photo_id = models.CharField(max_length=50, primary_key=True)  # 作品id
    caption = models.CharField(max_length=500,
                               default="Default Caption")  # 作品标题
    cover = models.CharField(max_length=500, default="Default Cover")  # 作品封面
    play_url = models.CharField(max_length=500)  # 作品播放链接
    create_time = models.DateTimeField(default=0)  # 作品创建时间
    like_count = models.IntegerField(default=0)  # 作品点赞数
    comment_count = models.IntegerField(default=0)  # 作品评论数
    view_count = models.IntegerField(default=0)  # 作品观看数
    pending = models.BooleanField()  # 作品状态（是否正在处理，不能观看）
    labels = models.CharField(max_length=100, default="",
                              null=True)  # 表示视频的标签

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
    label_name = models.CharField(max_length=50)  # 标签名
    num = models.IntegerField(default=0)  # 该标签的video数

    class Meta:
        '''
        double linking: labels
        '''
        db_table = 'labels'


class Analyse(models.Model):
    '''
    表示一段时间内数量的统计值
    '''
    video = models.ForeignKey(Video,
                              on_delete=models.CASCADE,
                              related_name='analysis')  # 外键绑定视频
    user_id = models.CharField(max_length=50)  # 用户id
    sum_time = models.DateTimeField(default=0)
    total_view_count = models.IntegerField(default=0)
    total_comment_count = models.IntegerField(default=0)
    total_like_count = models.IntegerField(default=0)
