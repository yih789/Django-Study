from django.db import models

# 게시글 영역
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 숫자 영역 설정법
    # num_stars = models.IntegerField()
    
