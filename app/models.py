'''
这个文件定义了后端的两个类
'''

from django.db import models


class User(models.Model):
    '''
    用户类
    '''
    open_id = models.CharField(max_length=50, primary_key=True,
                               unique=True)  # 用户id，用户唯一标志
    public_count = models.IntegerField(default=0)  # 公开视频数量
    friend_count = models.IntegerField(default=0)  # 仅好友可见的视频数量
    private_count = models.IntegerField(default=0)  # 仅自己可见的视频数量
    all_count = models.IntegerField(default=0)  # 视频总量


class Video(models.Model):
    '''
    视频类
    '''
    user = models.CharField(max_length=50)  # 用户open_id
    photo_id = models.CharField(max_length=50)  # 作品id
    caption = models.CharField(max_length=500, default="NULL CAPTION")  # 作品标题
    cover = models.CharField(max_length=500, default="NULL COVER")  # 作品封面
    play_url = models.CharField(max_length=500)  # 作品播放链接
    create_time = models.DateTimeField(default=0)  # 作品创建时间
    like_count = models.IntegerField(default=0)  # 作品点赞数
    comment_count = models.IntegerField(default=0)  # 作品评论数
    view_count = models.IntegerField(default=0)  # 作品观看数
    pending = models.BooleanField()  # 作品状态（是否正在处理，不能观看）
