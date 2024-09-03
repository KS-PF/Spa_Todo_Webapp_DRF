from django.db import models
from accounts.models import CustomUserModel

PRIORITY_CHOICES = [
    (1, '低い'),
    (2, '普通'),
    (3, '高い'),
    (4, '緊急'),
]

class TodoModel(models.Model):
    id = models.AutoField('ID', primary_key=True)
    title = models.CharField('タイトル', max_length=48, blank=False, null=False)
    priority_status = models.IntegerField(
        '優先度',
        choices=PRIORITY_CHOICES,
        default=2,
    )
    is_complete = models.BooleanField('完了', default=False, null=False)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日',auto_now=True)
    created_by = models.ForeignKey(
        CustomUserModel, 
        on_delete=models.CASCADE, 
        related_name="todo_creater"
    )

    def __str__(self):
        todo_id = str(self.id)
        title = self.title
        priority = dict(PRIORITY_CHOICES).get(self.priority_status, '不明')
        return f"Todo ID:{todo_id} Title:{title} Priority:{priority}"

    class Meta:
        ordering = ['created_at']
        db_table = 'Todos'