'''
这个文件定义了后端的两个类
'''
import django.db


class User(django.db.models.Model):
    '''
    用户类
    '''
    open_id = django.db.models.CharField(max_length=50,
                                         primary_key=True)  # 用户id，用户唯一标志
    public_count = django.db.models.IntegerField(default=0)  # 公开视频数量
    friend_count = django.db.models.IntegerField(default=0)  # 仅好友可见的视频数量
    private_count = django.db.models.IntegerField(default=0)  # 仅自己可见的视频数量
    all_count = django.db.models.IntegerField(default=0)  # 视频总量


class Video(django.db.models.Model):
    '''
    视频类
    '''
    user = django.db.models.ForeignKey(
        User.open_id, on_delete=django.db.models.CASCADE)  # 用户
    photo_id = django.db.models.CharField(max_length=50)  # 作品id
    caption = django.db.models.CharField(max_length=500,
                                         default="NULL CAPTION")  # 作品标题
    cover = django.db.models.CharField(max_length=500,
                                       default="NULL COVER")  # 作品封面
    play_url = django.db.models.CharField(max_length=500)  # 作品播放链接
    create_time = django.db.models.DateTimeField(default=0)  # 作品创建时间
    like_count = django.db.models.IntegerField(default=0)  # 作品点赞数
    comment_count = django.db.models.IntegerField(default=0)  # 作品评论数
    view_count = django.db.models.IntegerField(default=0)  # 作品观看数
    pending = django.db.models.BooleanField()  # 作品状态（是否正在处理，不能观看）
