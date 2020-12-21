from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Job(models.Model):
    image = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    body = models.TextField()
    page_number = models.IntegerField()
    author =models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]