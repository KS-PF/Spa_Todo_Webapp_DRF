from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator



class CustomUserModel(AbstractUser):
    username = models.CharField('ユーザーID', 
                    max_length=48, 
                    unique=True, 
                    null=False,
                    validators=[RegexValidator(r'^(?=.*[a-z])(?=.*\d)[a-z\d]{8,48}$')],
                )
    email = models.EmailField('メールアドレス', max_length=254, unique=True, null=False)
    nick_name = models.CharField('ニックネーム', max_length=48, blank=False, null=False)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        db_table = 'CustomUsers'
