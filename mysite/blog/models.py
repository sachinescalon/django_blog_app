from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body=models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)

    # We have added a Meta class inside the model. This class defines metadata for the model. We use the
    # ordering attribute to tell Django that it should sort results by the publish field. This ordering will
    # apply by default for database queries when no specific order is provided in the query. We indicate
    # descending order by using a hyphen before the field name, -publish. Posts will be returned in reverse
    # chronological order by default.
    class Meta:
        ordering = ['-publish']


        # We have added the indexes option to the model’s Meta class. This option allows you to define database
        # indexes for your model, which could comprise one or multiple fields, in ascending or descending
        # order, or functional expressions and database functions. We have added an index for the publish
        # field. We use a hyphen before the field name to define the index in descending order. The creation of
        # this index will be included in the database migrations that we will generate later for our blog models.
        indexes = [
            models.Index(fields=['-publish']),
        ]

    
    
    def __str__(self) -> str:
        return self.title
