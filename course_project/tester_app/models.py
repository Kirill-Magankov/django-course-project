import datetime
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from slugify import slugify


# Create your models here.

def slugify_value(value): return slugify(value)


class Testing(models.Model):
    TYPE_CHOICES = (
        ('TEST', 'Тест'),
        ('INTERPRETER', 'Интерпретатор'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=150)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='TEST')
    slug = AutoSlugField(populate_from='name', unique=True, slugify=slugify_value)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('testing', kwargs={'test_slug': self.slug})

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Testing, on_delete=models.CASCADE)
    text_question = models.TextField(max_length=150)
    correct_answer = models.TextField(max_length=150)
    objects = models.Manager()

    def __str__(self):
        return self.text_question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.datetime.now().isoformat(sep=" ", timespec="seconds"))
    answer = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.is_correct = self.question.correct_answer == self.answer
        super().save(force_insert, force_update, using)

    def __str__(self):
        return self.answer
