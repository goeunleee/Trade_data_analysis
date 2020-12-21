from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Cloud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    uploadingdate = models.DateField(auto_now=True)
    subject = models.CharField(max_length=50, null=True)
    file = models.FileField(null=True)
    filetype = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    idx = models.AutoField(primary_key=True)

    def __str__(self):
        return self.subject

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
