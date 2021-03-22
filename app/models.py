'''
这个文件定义了后端的两个类
'''
from django.db import models


class User(models.Model):
    '''
    用户类
    '''
    _open_id = models.CharField(max_length=50, primary_key=True)  # 用户id，用户唯一标志
    _public_count = models.IntegerField(default=0)  # 公开视频数量
    _friend_count = models.IntegerField(default=0)  # 仅好友可见的视频数量
    _private_count = models.IntegerField(default=0)  # 仅自己可见的视频数量
    _all_count = models.IntegerField(default=0)  # 视频总量


class Video(models.Model):
    '''
    视频类
    '''
    _user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户
    _photo_id = models.CharField(max_length=50)  # 作品id
    _caption = models.CharField(max_length=500, default="NULL CAPTION")  # 作品标题
    _cover = models.CharField(max_length=500, default="NULL COVER")  # 作品封面
    _play_url = models.CharField(max_length=500)  # 作品播放链接
    _create_time = models.DateTimeField()  # 作品创建时间
    _like_count = models.IntegerField(default=0)  # 作品点赞数
    _comment_count = models.IntegerField(default=0)  # 作品评论数
    _view_count = models.IntegerField(default=0)  # 作品观看数
    _pending = models.BooleanField()  # 作品状态（是否正在处理，不能观看）
