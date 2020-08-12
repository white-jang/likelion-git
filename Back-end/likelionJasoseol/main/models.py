from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Jasoseol(models.Model):
    title = models.CharField(max_length=50) # 제목
    content = models.TextField() # 내용
    updated_at = models.DateTimeField(auto_now=True) # 현재 시간을 자동으로 저장
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # null 값 인정
    # 외래키로 연결된 object가 지워질 때 같이 지워진다
    # = 유저가 없어지면 유저가 작성한 자소설도 없어진다