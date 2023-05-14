from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    # 제목, 작성자, 내용, 카테고리, 첨부파일, 날짜
    title = models.CharField(max_length=200)
    #author = models.ForeignKey(User, on_delete=models.CASCADE, default="user")
    author = models.CharField(max_length=50, default="diary") # 이 부분은 우선 User 모델을 생성하지 않았기 때문에 일시적으로 저장
    content = models.TextField()
    category = models.CharField(max_length=50, default="diary")
    addFile = models.FileField(upload_to='uploads/', null=True, blank=True)
    write_date = models.DateTimeField()

    def __str__(self):
        return self.title