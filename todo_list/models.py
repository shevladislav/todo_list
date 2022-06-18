from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_detail', args=(
            self.pk,
            self.title,
            self.author,
            self.date_create.year,
            self.date_create.month,
            self.date_create.day,
        ))

    def get_absolute_url_for_delete(self):
        return reverse('task_delete', args=(
            self.pk,
            self.title,
            self.author,
            self.date_create.year,
            self.date_create.month,
            self.date_create.day,
        ))
