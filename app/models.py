from django.db import models

class User(models.Model):
    open_id = models.CharField(max_length=50,primary_key=True)
    public_count = models.IntegerField(default=0)
    friend_count = models.IntegerField(default=0)
    private_count = models.IntegerField(default=0)
    all_count = models.IntegerField(default=0)

class Video(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    photo_id = models.CharField(max_length=50)
    caption = models.CharField(max_length=500,default="NULL CAPTION")
    cover = models.CharField(max_length=500,default="NULL COVER")
    play_url = models.CharField(max_length=500)
    create_time = models.DateTimeField()
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    pending = models.BooleanField()
