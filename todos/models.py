from django.db import models
from accounts.models import CustomUserModel


PRIORITY_CHOICES = [
    ('低い', '低い'),
    ('普通', '普通'),
    ('高い', '高い'),
    ('緊急', '緊急'),
]

class  TodoModel(models.Model):
    id = models.AutoField('ID', primary_key=True)
    title = models.CharField('タイトル', max_length=48, blank=False, null=False)
    priority_status = models.CharField(
        '優先度',
        max_length=4,
        choices=PRIORITY_CHOICES,
        default='普通',
    )
    is_complete = models.BooleanField('完了', default=False, null=False)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日',auto_now=True)
    created_by = models.ForeignKey(
        CustomUserModel, 
        on_delete=models.CASCADE, 
        related_name = "todo_creater"
    )

    def __str__(self):
        todo_id = str(self.id)
        title = self.title
        return f"Todo ID:{todo_id} Title:{title}"

    class Meta:
        ordering = ['created_at']
        db_table = 'Todos'
