import uuid

from django.db import models
from django.core.files.storage import FileSystemStorage


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'


class Question(BaseModel):
    question = models.TextField()

    def __str__(self):
        return self.question


class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return self.answer


class TrainingFile(BaseModel):
    file = models.FileField(upload_to='training')
    is_ran = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name
